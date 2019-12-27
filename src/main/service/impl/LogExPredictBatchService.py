#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import json
import pickle
import datetime
import numpy as np
import pandas as pd
from src.main.utils.RedisUtil import RedisUtil
from src.main.service.TrainingService import TrainingService
from src.main.utils.LogAlertProcessUtil import LogAlertProcessUtil
from src.main.utils.LogAlertPredictUtil import LogAlertPredictUtil
from src.main.utils.LogAlertTrainUtil import LogAlertTrainUtil
from sklearn.metrics.pairwise import cosine_distances
from src.main.domain.vo.LogAlertReturn import SingleSimilarRes
from src.main.domain.vo.LogAlertFeedBack import Feedback,SingleResult
from src.main.utils.HttpUtil import HttpUtil
from src.main import myGlobal
from distutils.util import strtobool
from src.main.domain.vo.LogAlertBatchReturn import LogAlertBatchReturn
# from memory_profiler import profile
from src.main.utils import ConfigurationUtil

class LogAlertPredictBatchService(TrainingService):
    def __init__(self):
        super().__init__()
        self.deployModel = str(ConfigurationUtil.get('LogAlert','deployMode'))
        self.rootPath = myGlobal.getConfigByName('LogAlert_rootPath')
        self.feedbackUrl = myGlobal.getConfigByName('FeedBack_url')
        self.sendOrNotSend = strtobool(myGlobal.getConfigByName('FeedBack_sendOrNotSend'))
        self.saveUnKnown = strtobool(myGlobal.getConfigByName('FeedBack_saveUnKnown'))


    # @profile
    def make_procedure(self, trackingIds):
        res = []
        feedback = []

        for trackingId in trackingIds:
            similarResAdjust = []
            keyWords = []
            predictTag = trackingId.desc.component + '&' + trackingId.desc.servertype
            unknownDist = float(myGlobal.getConfigByName('LogAlert_unknownDist',predictTag))
            LogAlertProcessUtil = LogAlertProcessUtil(predictTag)

            if (self.deployModel == 'local'):
                if not predictTag in myGlobal.targetSplited.keys(): continue
                if not str('d2v_dbow_'+predictTag) in myGlobal.d2vModel.keys(): continue
                if not str('w2v_'+predictTag) in myGlobal.w2vModel.keys(): continue
                targetSplited = myGlobal.targetSplited[predictTag]
                d2vModel = myGlobal.d2vModel['d2v_dbow_' + predictTag]
                w2vModel = myGlobal.w2vModel['w2v_' + predictTag]
            else:
                if not RedisUtil().keyExists('d2v_dbow_' + predictTag): continue
                if not RedisUtil().keyExists('w2v_' + predictTag): continue
                if not RedisUtil().keyExists(predictTag): continue
                d2vModel = pickle.loads(RedisUtil().get_single_data('d2v_dbow_' + predictTag))
                w2vModel = pickle.loads(RedisUtil().get_single_data('w2v_' + predictTag))
                targetSplited = pickle.loads(RedisUtil().get_single_data(predictTag))

            LogAlertPredictutil = LogAlertPredictUtil(self.rootPath, 'batchPredict&'+LogAlertProcessUtil.getHostName())
            predSplited = LogAlertPredictutil.genPredSplited([trackingId])

            if predSplited.tolist():
                # del predDF,predSplited,predictLog,targetDF,targetSplited,targetLog,d2vModel,w2vModel
                # gc.collect()
                targetDF, d2vModel, w2vModel = LogAlertPredictutil.genTargetDF(targetSplited, predictTag, d2vModel,w2vModel)
                predDF, d2vModel, w2vModel = LogAlertPredictutil.genPredDF(predSplited, d2vModel, w2vModel)

                if (self.deployModel == 'local'):
                    myGlobal.d2vModel['d2v_dbow_' + predictTag] = d2vModel
                    myGlobal.w2vModel['w2v_' + predictTag] = w2vModel
                else:
                    RedisUtil().set_single_data('d2v_dbow_' + predictTag, pickle.dumps(d2vModel))
                    RedisUtil().set_single_data('w2v_' + predictTag, pickle.dumps(w2vModel))

                dist = []
                for i in range(0, targetDF.shape[0]):
                    dist.append([i, cosine_distances(np.array([predDF.iloc[0], targetDF.iloc[i]]))[0][1]])
                result_temp = pd.DataFrame(dist, columns=["index", "distance"]).sort_values("distance")
                rawData = LogAlertTrainUtil(self.rootPath, 'target_' + predictTag).genRawData()
                result = pd.merge(rawData.reset_index(), result_temp).drop(columns=['log', 'Unnamed: 0', 'level_0']).sort_index(by=['distance'], ascending=True)

                trackingId_CosDist = {}
                similarRes = []
                i = 1
                for index, row in result.iterrows():
                    similarRes.append(SingleSimilarRes(row['id'], row['tag'][0], row['distance'], i).__dict__)
                    trackingId_CosDist[row['id']] = float(row['distance'])
                    i = i + 1

                targetLog = pd.read_csv(str(self.rootPath + '/LogAlert/input/resFilter_%s.csv' % ('target_' + predictTag)))
                predictLog = pd.read_csv(self.rootPath + '/LogAlert/input/resFilter_batchPredict&' + LogAlertProcessUtil.getHostName() + '.csv')
                keyWordsColForPredict = LogAlertProcessUtil.findUniqueKeywords(LogAlertProcessUtil.splitWordSentenceForKeyWords(LogAlertProcessUtil.conc_list(predictLog['log'].values.tolist()),'List'))

                trackingId_levenDist = {}
                for targetTrackingId in result['id']:
                    logs = []
                    for index, row in targetLog.iterrows():
                        if (row['id'] == targetTrackingId):
                            logs.append(row['log'])
                    keyWordsColForTarget = LogAlertProcessUtil.findUniqueKeywords(LogAlertProcessUtil.splitWordSentenceForKeyWords(LogAlertProcessUtil.conc_list(logs), 'List'))
                    trackingId_levenDist[targetTrackingId] = LogAlertProcessUtil.simlarityCal(keyWordsColForTarget,keyWordsColForPredict)

                trackingId_dist_df = pd.DataFrame(columns=['trackingId', 'dist'])
                for (k, v) in trackingId_CosDist.items():
                    print('targetTrackingId is '+ k + 'cos distance is '+str(v)+' lenven distance is '+str(trackingId_levenDist[k]))
                    trackingId_dist_df = trackingId_dist_df.append({'trackingId': k, 'dist': v + trackingId_levenDist[k]},ignore_index=True)

                for index, row in trackingId_dist_df.sort_index(by=['dist'], ascending=True).iterrows():
                    id = row['trackingId']
                    for singleSimilarRes in similarRes:
                        if singleSimilarRes['trackingId'] == id:
                            singleSimilarRes['distance'] = row['dist']
                            similarResAdjust.append(singleSimilarRes)
                distance = similarResAdjust[0]['distance']
                tag = similarResAdjust[0]['tag'] if float(similarResAdjust[0]['distance']) < unknownDist else 'Unknown'
                if (tag=='Unknown'):
                    keyWords = keyWordsColForPredict
                    if self.saveUnKnown: self.saveUnKnownTrackingId(trackingId, pd.DataFrame(predictLog[predictLog['id']==trackingId.name], columns=['id', 'log']))
                feedback.append(SingleResult(trackingId.desc.component, trackingId.desc.servertype, tag, trackingId.name,similarResAdjust[0]['trackingId']).__dict__)
            else:
                distance = '100'
                tag = 'Not Found'

            # del predDF,predSplited,predictLog,targetDF,targetSplited,targetLog,d2vModel,w2vModel
            # gc.collect()
            res.append(LogAlertBatchReturn(name=trackingId.name,tag=tag,distance=distance,keyWords=keyWords,desc=trackingId.desc.__dict__).__dict__)

        if (self.sendOrNotSend):
            try:
                response = HttpUtil().post(json.dumps(Feedback(feedback).__dict__),self.feedbackUrl)
                print(response)
            except Exception as e:
                print("send feedback fail " + str(e))

        return res

    def saveUnKnownTrackingId(self,trackingId,unknownDF):
        rootPath = self.rootPath
        rawDataDirPath = rootPath + '/LogAlert/input/' + str(datetime.date.today())
        if not os.path.exists(rawDataDirPath): os.mkdir(rawDataDirPath)
        rawDataFilePath = rawDataDirPath + '/unkonwn_%s.csv' % (trackingId.desc.component + '&' + trackingId.desc.servertype)
        if not os.path.exists(rawDataFilePath):
            unknownDF.to_csv(rawDataFilePath, index=False)
        else:
            unknownDF.to_csv(rawDataFilePath, mode='a', header=False, index=False)
        return


