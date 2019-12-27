#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import csv
import datetime
import pickle
from src.main.service.TrainingService import TrainingService
from src.main.utils.TimeUtil import Timeutil
from src.main.utils.LogAlertTrainUtil import LogAlertTrainUtil
from src.main.utils.RedisUtil import RedisUtil
from src.main.domain.vo.LogAlertTrackingId import LogAlertTrackingId,Desc
from src.main import myGlobal
from src.main.utils import ConfigurationUtil

class LogAlertTrainService(TrainingService):
    def __init__(self):
        super().__init__()
        self.timeUtil = Timeutil()
        self.rootPath = myGlobal.getConfigByName('LogAlert_rootPath')
        self.deployModel = ConfigurationUtil.get('LogAlert', 'deployMode')

    def make_procedure_post(self,trainFiles):
        for trainFile in trainFiles:
            trainTag = trainFile.component+'&'+trainFile.servertype+'&'+trainFile.tag
            LogAlertTrainUtil = LogAlertTrainUtil(self.rootPath,trainTag)
            LogAlertTrainUtil.genFilterFileByFilePathOnMutiproc(trainFile.component,trainFile.servertype,trainFile.path)
            splited = LogAlertTrainUtil.genSplitedData()
            LogAlertTrainUtil.genTrainDataForD2V(splited)
            self.loadModel('d2v_dbow_' + trainFile.component+'&'+trainFile.servertype,LogAlertTrainUtil.genD2VModelByDBOW(),'w2v_' + trainFile.component+'&'+trainFile.servertype,LogAlertTrainUtil.genW2VModel(splited))
        return

    def make_procedure_request(self,trainSize):
        realTrainSize = min([int(trainSize),len([lists for lists in os.listdir(self.rootPath+'/LogAlert/rawdata') if os.path.isdir(os.path.join(self.rootPath+'/LogAlert/rawdata', lists))])])
        trainDirs = self.timeUtil.getDateRange(str(datetime.date.today()-datetime.timedelta(days=int(realTrainSize))),self.timeUtil.getYesterday())
        for trainDir in trainDirs:
            trainDict = {}
            for rawDataFile in os.listdir(self.rootPath+'/LogAlert/rawdata/%s'%(trainDir)):
                trainTag = rawDataFile.split('.')[0].split('_')[1]
                dataline = csv.reader(open(self.rootPath+'/LogAlert/rawdata/%s'%(trainDir+'/'+rawDataFile), 'r'))
                trackingIds = []
                for i in dataline:
                    if dataline.line_num == 1:
                        continue
                    trackingIds.append(LogAlertTrackingId(i[0], '', Desc(trainTag.split('&')[0], trainTag.split('&')[1], i[1])))
                if not trainTag in trainDict.keys():
                    trainDict[trainTag] = list(set(trackingIds))
                else:
                    tmplist = trainDict.get(trainTag)
                    tmplist.extend(trackingIds)
                    trainDict[trainTag] = list(set(tmplist))

        for (k,v) in trainDict.items():
            LogAlertTrainUtil = LogAlertTrainUtil(self.rootPath, k)
            LogAlertTrainUtil.genFilterFileBytrackingIdsByMutiproc(v)
            splited = LogAlertTrainUtil.genSplitedData()
            LogAlertTrainUtil.genTrainDataForD2V(splited)
            self.loadModel('d2v_dbow_' + k,LogAlertTrainUtil.genD2VModelByDBOW(),'w2v_' + k,LogAlertTrainUtil.genW2VModel(splited))
        return

    def loadModel(self,d2vModelName,d2vModel,w2vModelName,w2vmodel):
        if (self.deployModel == 'local'):
            if (myGlobal.d2vModel == None):
                myGlobal.d2vModel = {d2vModelName: d2vModel}
            else:
                myGlobal.d2vModel[d2vModelName] = d2vModel

            if (myGlobal.w2vModel == None):
                myGlobal.w2vModel = {w2vModelName: w2vmodel}
            else:
                myGlobal.w2vModel[w2vModelName] = w2vmodel
        else:
            RedisUtil().set_single_data(d2vModelName, pickle.dumps(d2vModel))
            RedisUtil().set_single_data(w2vModelName, pickle.dumps(w2vmodel))
