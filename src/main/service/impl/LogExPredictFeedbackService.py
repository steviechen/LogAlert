#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from src.main.service.TrainingService import TrainingService
from src.main.utils.TimeUtil import Timeutil
from src.main.utils.LogExTrainUtil import LogExTrainUtil
from src.main.domain.vo.LogExTrackingId import LogExTrackingId,Desc
from src.main.utils.LogExProcessUtil import LogExProcessUtil
from src.main.domain.vo.LogExClusterReturn import LogExClusterReturn,SingleResult,Topic
from gensim import corpora, models
from src.main import myGlobal

class LogExPredictFeedbackService(TrainingService):
    def __init__(self):
        super().__init__()
        self.timeUtil = Timeutil()
        self.rootPath = myGlobal.getConfigByName('LogEx_rootPath')
        self.unknownDataDir = self.rootPath+'/Logex/input'

    def make_procedure(self,trackingIds,clusterNum,topN):
        rawData = pd.DataFrame(columns=['name', 'component', 'servertype', 'dc'])
        for trackingId in trackingIds:
            rawData = rawData.append({'name': trackingId.name, 'component': trackingId.desc.component,'servertype': trackingId.desc.servertype, 'dc': trackingId.desc.dc},ignore_index=True)

        feedback = []
        for name,group in rawData.groupby(['component','servertype']):
            logExProcessUtil = LogExProcessUtil(name[0] + '&' + name[1])
            trainTag = str('unknown_' + name[0] + '&' + name[1] + '&' + logExProcessUtil.getHostName())
            logExTrainUtil = LogExTrainUtil(self.rootPath, trainTag)
            singleTypeTrackingIds = []
            for index, row in group.iterrows():
                singleTypeTrackingIds.append(LogExTrackingId(row['name'],'', Desc(row['component'], row['servertype'], row['dc'])))
            logExTrainUtil.genFilterFileBytrackingIdsByMutiproc(singleTypeTrackingIds)
            unknownLogs = []
            for singleLog in pd.read_csv(self.unknownDataDir + '/resFilter_%s.csv'%(trainTag))['log'].values.tolist():
                unknownLogs.append(logExProcessUtil.findKeywords(logExProcessUtil.splitWordSentenceForKeyWords(singleLog,'List')))
            feedback.append(SingleResult(name[0],name[1],self.genClusterRes(unknownLogs,clusterNum,topN)).__dict__)
        return LogExClusterReturn(feedback).__dict__

    def genClusterRes(self,texts,clusterNum,topN):
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        lda = models.LdaModel(corpus=models.TfidfModel(corpus)[corpus], id2word=dictionary, num_topics=clusterNum, passes=30)
        topics = []
        for i in range(clusterNum):
            clusterRes = [j[0] for j in lda.show_topic(topn=topN, topicid=i)]
            topics.append(Topic(str(i+1),clusterRes).__dict__)
        return topics
