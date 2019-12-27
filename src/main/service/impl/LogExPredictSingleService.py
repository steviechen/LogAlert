#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pickle
import datetime
import json
import numpy as np
import pandas as pd
from src.main.service.TrainingService import TrainingService
from src.main.utils.LogExProcessUtil import LogExProcessUtil
from src.main.utils.LogExPredictUtil import LogExPredictUtil
from src.main.utils.RedisUtil import RedisUtil
from src.main.utils.LogExTrainUtil import LogExTrainUtil
from sklearn.metrics.pairwise import cosine_distances
from src.main.domain.vo.LogExReturn import LogExReturn,PredictDetail,TargetDetail,SingleSimilarRes
from src.main.domain.vo.LogExFeedBack import Feedback,SingleResult
from src.main.domain.vo.Message import Message
from src.main.utils.HttpUtil import HttpUtil
from src.main import myGlobal
from distutils.util import strtobool
from src.main.utils import ConfigurationUtil

class LogExPredictSingleService(TrainingService):
    def __init__(self):
        super().__init__()
        self.deployModel = str(ConfigurationUtil.get('LogEx','deployMode'))
        self.rootPath = myGlobal.getConfigByName('LogEx_rootPath')
        self.feedbackUrl = myGlobal.getConfigByName('FeedBack_url')
        self.sendOrNotSend = strtobool(myGlobal.getConfigByName('FeedBack_sendOrNotSend'))
        self.saveUnKnown = strtobool(myGlobal.getConfigByName('FeedBack_saveUnKnown'))

    def make_procedure(self,trackingId):
        predictTag = trackingId.desc.component+'&'+trackingId.desc.servertype
        unknownDist = float(myGlobal.getConfigByName('LogEx_unknownDist',predictTag))
        logExProcessUtil = LogExProcessUtil(predictTag)
        if (self.deployModel == 'local'):
            if not str('d2v_dbow_'+predictTag) in myGlobal.d2vModel.keys():
                return Message("can not find the d2vModel for %s!"%(predictTag)).__dict__
            else:
                d2vModel = myGlobal.d2vModel['d2v_dbow_' + predictTag]

            if not str('w2v_'+predictTag) in myGlobal.w2vModel.keys():
                return Message("can not find the w2vModel for %s!"%(predictTag)).__dict__
            else:
                w2vModel = myGlobal.w2vModel['w2v_' + predictTag]

            if not predictTag in myGlobal.targetSplited.keys():
                return Message("can not find the targetTrackingIds result for %s!" % (predictTag)).__dict__
            else:
                targetSplited = myGlobal.targetSplited[predictTag]
        else:
            if not RedisUtil().keyExists('d2v_dbow_' + predictTag):
                return Message("can not find the d2vModel in redis for %s!" % (predictTag)).__dict__
            else:
                d2vModel = pickle.loads(RedisUtil().get_single_data('d2v_dbow_' + predictTag))

            if not RedisUtil().keyExists('w2v_' + predictTag):
                return Message("can not find the w2vModel in redis for %s!" % (predictTag)).__dict__
            else:
                w2vModel = pickle.loads(RedisUtil().get_single_data('w2v_' + predictTag))

            if not RedisUtil().keyExists(predictTag):
                return Message("can not find the targetTrackingIds result in redis for %s!" % (predictTag)).__dict__
            else:
                targetSplited = pickle.loads(RedisUtil().get_single_data(predictTag))

        logExPredictutil = LogExPredictUtil(self.rootPath, 'SinglePredict&'+logExProcessUtil.getHostName())
        predSplited = logExPredictutil.genPredSplited([trackingId])
        if not predSplited.tolist() : return Message("can not find the log info for %s in ES"% trackingId.name).__dict__
        targetDF,d2vModel,w2vModel = logExPredictutil.genTargetDF(targetSplited,predictTag,d2vModel,w2vModel)
        predDF,d2vModel,w2vModel = logExPredictutil.genPredDF(predSplited,d2vModel,w2vModel)

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
        rawData = LogExTrainUtil(self.rootPath,'target_'+predictTag).genRawData()
        result = pd.merge(rawData.reset_index(), result_temp).drop(columns=['log','Unnamed: 0','level_0']).sort_index(by=['distance'],ascending=True)
        trackingId_CosDist = {}
        similarRes = []
        i = 1
        for index,row in result.iterrows():
            similarRes.append(SingleSimilarRes(row['id'],row['tag'][0],row['distance'],i).__dict__)
            trackingId_CosDist[row['id']] = float(row['distance'])
            i=i+1

        predictLog = pd.read_csv(self.rootPath+'/Logex/input/resFilter_SinglePredict&'+logExProcessUtil.getHostName()+'.csv')
        targetLog = pd.read_csv(self.rootPath+'/Logex/input/resFilter_%s.csv'%('target_'+predictTag))
        keyWordsColForPredict = logExProcessUtil.findUniqueKeywords(logExProcessUtil.splitWordSentenceForKeyWords(logExProcessUtil.conc_list(predictLog['log'].values.tolist()),'List'))

        trackingId_levenDist = {}
        targetDetails = []
        for targetTrackingId in result['id']:
            logs = []
            for index,row in targetLog.iterrows():
                if(row['id']==targetTrackingId):
                    logs.append(row['log'])
            keyWords = logExProcessUtil.findUniqueKeywords(logExProcessUtil.splitWordSentenceForKeyWords(logExProcessUtil.conc_list(logs),'List'))
            targetDetails.append(TargetDetail(targetTrackingId,logs,keyWords).__dict__)
            trackingId_levenDist[targetTrackingId] = logExProcessUtil.simlarityCal(keyWords,keyWordsColForPredict)

        trackingId_dist_df = pd.DataFrame(columns=['trackingId', 'dist'])
        for (k, v) in trackingId_CosDist.items():
            print('targetTrackingId is '+ k +'cos distance is ' + str(v) + ' lenven distance is ' + str(trackingId_levenDist[k]))
            trackingId_dist_df = trackingId_dist_df.append({'trackingId':k,'dist':v+trackingId_levenDist[k]},ignore_index=True)

        similarResAdjust = []
        targetDetailsAdjust = []
        j = 1
        for index,row in trackingId_dist_df.sort_index(by=['dist'],ascending=True).iterrows():
            id = row['trackingId']
            for singleSimilarRes in similarRes:
                if singleSimilarRes['trackingId']==id:
                    singleSimilarRes['distance']=row['dist']
                    singleSimilarRes['sort']=str(j)
                    similarResAdjust.append(singleSimilarRes)
            for targetDetail in targetDetails:
                if targetDetail['trackingId']==id: targetDetailsAdjust.append(targetDetail)
            j=j+1

        targetTrackingId = similarResAdjust[0]['trackingId']
        predictLabel = similarResAdjust[0]['tag'] if float(similarResAdjust[0]['distance']) < unknownDist else 'Unknown'

        if(self.sendOrNotSend):
            try:
                feedback = []
                feedback.append(SingleResult(trackingId.desc.component, trackingId.desc.servertype, predictLabel,trackingId.name,targetTrackingId).__dict__)
                response = HttpUtil().post(json.dumps(Feedback(feedback).__dict__), self.feedbackUrl)
                print(response)
            except Exception as e:
                print("send feedback fail " + str(e))

        if predictLabel == 'Unknown':
            if(self.saveUnKnown):self.saveUnKnownTrackingId(trackingId,pd.DataFrame(predictLog,columns=['id','log']))
            return LogExReturn('No trackingId retrieved',similarResAdjust,PredictDetail(trackingId.name,predictLog['log'].tolist(),keyWordsColForPredict).__dict__,targetDetailsAdjust).__dict__
        else:
            return LogExReturn('trackingId retrieved',similarResAdjust,PredictDetail(trackingId.name,predictLog['log'].tolist(),keyWordsColForPredict).__dict__,targetDetailsAdjust).__dict__


    def saveUnKnownTrackingId(self,trackingId,unknownDF):
        rootPath = self.rootPath
        rawDataDirPath = rootPath + '/Logex/input/' + str(datetime.date.today())
        if not os.path.exists(rawDataDirPath): os.mkdir(rawDataDirPath)
        rawDataFilePath = rawDataDirPath + '/unkonwn_%s.csv' % (trackingId.desc.component + '&' + trackingId.desc.servertype)
        if not os.path.exists(rawDataFilePath):
            unknownDF.to_csv(rawDataFilePath, index=False)
        else:
            unknownDF.to_csv(rawDataFilePath, mode='a', header=False, index=False)
        return

