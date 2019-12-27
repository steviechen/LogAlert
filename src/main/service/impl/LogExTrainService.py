#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import csv
import datetime
import pickle
from src.main.service.TrainingService import TrainingService
from src.main.utils.TimeUtil import Timeutil
from src.main.utils.LogExTrainUtil import LogExTrainUtil
from src.main.utils.RedisUtil import RedisUtil
from src.main.domain.vo.LogExTrackingId import LogExTrackingId,Desc
from src.main import myGlobal
from src.main.utils import ConfigurationUtil

class LogExTrainService(TrainingService):
    def __init__(self):
        super().__init__()
        self.timeUtil = Timeutil()
        self.rootPath = myGlobal.getConfigByName('LogEx_rootPath')
        self.deployModel = ConfigurationUtil.get('LogEx', 'deployMode')

    def make_procedure_post(self,trainFiles):
        for trainFile in trainFiles:
            trainTag = trainFile.component+'&'+trainFile.servertype+'&'+trainFile.tag
            logExTrainUtil = LogExTrainUtil(self.rootPath,trainTag)
            logExTrainUtil.genFilterFileByFilePathOnMutiproc(trainFile.component,trainFile.servertype,trainFile.path)
            splited = logExTrainUtil.genSplitedData()
            logExTrainUtil.genTrainDataForD2V(splited)
            self.loadModel('d2v_dbow_' + trainFile.component+'&'+trainFile.servertype,logExTrainUtil.genD2VModelByDBOW(),'w2v_' + trainFile.component+'&'+trainFile.servertype,logExTrainUtil.genW2VModel(splited))
        return

    def make_procedure_request(self,trainSize):
        realTrainSize = min([int(trainSize),len([lists for lists in os.listdir(self.rootPath+'/Logex/rawdata') if os.path.isdir(os.path.join(self.rootPath+'/Logex/rawdata', lists))])])
        trainDirs = self.timeUtil.getDateRange(str(datetime.date.today()-datetime.timedelta(days=int(realTrainSize))),self.timeUtil.getYesterday())
        for trainDir in trainDirs:
            trainDict = {}
            for rawDataFile in os.listdir(self.rootPath+'/Logex/rawdata/%s'%(trainDir)):
                trainTag = rawDataFile.split('.')[0].split('_')[1]
                dataline = csv.reader(open(self.rootPath+'/Logex/rawdata/%s'%(trainDir+'/'+rawDataFile), 'r'))
                trackingIds = []
                for i in dataline:
                    if dataline.line_num == 1:
                        continue
                    trackingIds.append(LogExTrackingId(i[0], '', Desc(trainTag.split('&')[0], trainTag.split('&')[1], i[1])))
                if not trainTag in trainDict.keys():
                    trainDict[trainTag] = list(set(trackingIds))
                else:
                    tmplist = trainDict.get(trainTag)
                    tmplist.extend(trackingIds)
                    trainDict[trainTag] = list(set(tmplist))

        for (k,v) in trainDict.items():
            logExTrainUtil = LogExTrainUtil(self.rootPath, k)
            logExTrainUtil.genFilterFileBytrackingIdsByMutiproc(v)
            splited = logExTrainUtil.genSplitedData()
            logExTrainUtil.genTrainDataForD2V(splited)
            self.loadModel('d2v_dbow_' + k,logExTrainUtil.genD2VModelByDBOW(),'w2v_' + k,logExTrainUtil.genW2VModel(splited))
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
