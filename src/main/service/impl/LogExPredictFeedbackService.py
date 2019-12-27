#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pandas as pd
from src.main.service.TrainingService import TrainingService
from src.main.utils.TimeUtil import Timeutil
from src.main.utils.LogAlertTrainUtil import LogAlertTrainUtil
from src.main.domain.vo.LogAlertTrackingId import LogAlertTrackingId,Desc
from src.main.utils.LogAlertProcessUtil import LogAlertProcessUtil
from src.main.domain.vo.LogAlertClusterReturn import LogAlertClusterReturn,SingleResult,Topic
from gensim import corpora, models
from src.main import myGlobal

class LogAlertPredictFeedbackService(TrainingService):
    def __init__(self):
        super().__init__()
        self.timeUtil = Timeutil()
        self.rootPath = myGlobal.getConfigByName('LogAlert_rootPath')
        self.unknownDataDir = self.rootPath+'/LogAlert/input'

    def make_procedure(self,trackingIds,clusterNum,topN):
        rawData = pd.DataFrame(columns=['name', 'component', 'servertype', 'dc'])
        for trackingId in trackingIds:
            rawData = rawData.append({'name': trackingId.name, 'component': trackingId.desc.component,'servertype': trackingId.desc.servertype, 'dc': trackingId.desc.dc},ignore_index=True)

        feedback = []
        for name,group in rawData.groupby(['component','servertype']):
            LogAlertProcessUtil = LogAlertProcessUtil(name[0] + '&' + name[1])
            trainTag = str('unknown_' + name[0] + '&' + name[1] + '&' + LogAlertProcessUtil.getHostName())
            LogAlertTrainUtil = LogAlertTrainUtil(self.rootPath, trainTag)
            singleTypeTrackingIds = []
            for index, row in group.iterrows():
                singleTypeTrackingIds.append(LogAlertTrackingId(row['name'],'', Desc(row['component'], row['servertype'], row['dc'])))
            LogAlertTrainUtil.genFilterFileBytrackingIdsByMutiproc(singleTypeTrackingIds)
            unknownLogs = []
            for singleLog in pd.read_csv(self.unknownDataDir + '/resFilter_%s.csv'%(trainTag))['log'].values.tolist():
                unknownLogs.append(LogAlertProcessUtil.findKeywords(LogAlertProcessUtil.splitWordSentenceForKeyWords(singleLog,'List')))
            feedback.append(SingleResult(name[0],name[1],self.genClusterRes(unknownLogs,clusterNum,topN)).__dict__)
        return LogAlertClusterReturn(feedback).__dict__

    def genClusterRes(self,texts,clusterNum,topN):
        dictionary = corpora.Dictionary(texts)
        corpus = [dictionary.doc2bow(text) for text in texts]
        lda = models.LdaModel(corpus=models.TfidfModel(corpus)[corpus], id2word=dictionary, num_topics=clusterNum, passes=30)
        topics = []
        for i in range(clusterNum):
            clusterRes = [j[0] for j in lda.show_topic(topn=topN, topicid=i)]
            topics.append(Topic(str(i+1),clusterRes).__dict__)
        return topics
