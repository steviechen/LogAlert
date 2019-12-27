#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pickle
import pandas as pd
from src.main.service.TrainingService import TrainingService
from src.main.utils.TimeUtil import Timeutil
from src.main.utils.LogAlertTrainUtil import LogAlertTrainUtil
from src.main.domain.vo.LogAlertTrackingId import LogAlertTrackingId,Desc
from src.main.utils.RedisUtil import RedisUtil
from src.main import myGlobal
from src.main.utils import ConfigurationUtil

class LogAlertLoadTargetTrackingIdService(TrainingService):
    def __init__(self):
        super().__init__()
        self.timeUtil = Timeutil()
        self.rootPath = myGlobal.getConfigByName('LogAlert_rootPath')
        self.deployModel = str(ConfigurationUtil.get('LogAlert','deployMode'))

    def make_procedure(self,trackingIds,processWay):
        rawData = pd.DataFrame(columns=['name', 'component', 'servertype', 'dc', 'tag'])
        for trackingId in trackingIds:
            rawData = rawData.append({'name': trackingId.name, 'tag': trackingId.tag, 'component': trackingId.desc.component,'servertype': trackingId.desc.servertype, 'dc': trackingId.desc.dc}, ignore_index=True)

        if processWay == 'load':
            if not len(trackingIds):
                for resfile in os.listdir(self.rootPath+'/LogAlert/input'):
                    if resfile.startswith('resFilter_target'):
                        component = resfile.split('.')[0].split('&')[0].split('_')[2]
                        serverType = resfile.split('.')[0].split('&')[1]
                        LogAlertTrainUtil = LogAlertTrainUtil(self.rootPath, str('target_' + component + '&' + serverType))
                        targetSplited = LogAlertTrainUtil.genSplitedData()
                        LogAlertTrainUtil.genTrainDataForD2V(targetSplited)
                        self.loadTargetTrackingId(component,serverType,targetSplited)

            for name,group in rawData.groupby(['component','servertype']):
                LogAlertTrainUtil = LogAlertTrainUtil(self.rootPath,str('target_'+name[0]+'&'+name[1]))
                singleTypeTrackingIds = []
                for index,row in group.iterrows():
                    singleTypeTrackingIds.append(LogAlertTrackingId(row['name'],row['tag'],Desc(row['component'],row['servertype'],row['dc'])))

                LogAlertTrainUtil.genFilterFileBytrackingIdsByMutiproc(singleTypeTrackingIds)
                targetSplited = LogAlertTrainUtil.genSplitedData()
                LogAlertTrainUtil.genTrainDataForD2V(targetSplited)
                self.loadTargetTrackingId(name[0], name[1], targetSplited)

        if processWay =='append':
            for name,group in rawData.groupby(['component','servertype']):
                LogAlertTrainUtil = LogAlertTrainUtil(self.rootPath,str('target_'+name[0]+'&'+name[1]))
                existTargetTrackingIds = LogAlertTrainUtil.getAllTrackingId()
                singleTypeTrackingIds = []
                for index,row in group.iterrows():
                    if row['name'] not in existTargetTrackingIds:
                        singleTypeTrackingIds.append(LogAlertTrackingId(row['name'],row['tag'],Desc(row['component'],row['servertype'],row['dc'])))

                if len(singleTypeTrackingIds):LogAlertTrainUtil.appendFilterFileBytrackingIdsByMutiproc(singleTypeTrackingIds)
                targetSplited = LogAlertTrainUtil.genSplitedData()
                LogAlertTrainUtil.genTrainDataForD2V(targetSplited)
                self.loadTargetTrackingId(name[0],name[1],targetSplited)

        if processWay =='delete':
            for name,group in rawData.groupby(['component','servertype']):
                LogAlertTrainUtil = LogAlertTrainUtil(self.rootPath,str('target_'+name[0]+'&'+name[1]))
                singleTypeTrackingIds = []
                for index, row in group.iterrows():
                    singleTypeTrackingIds.append(LogAlertTrackingId(row['name'], row['tag'], Desc(row['component'], row['servertype'], row['dc'])))

                LogAlertTrainUtil.deleteByTrackingId(singleTypeTrackingIds)
                targetSplited = LogAlertTrainUtil.genSplitedData()
                LogAlertTrainUtil.genTrainDataForD2V(targetSplited)
                self.loadTargetTrackingId(name[0],name[1],targetSplited)

        return

    def loadTargetTrackingId(self,component,serverType,targetSplited):
        if (self.deployModel == 'local'):
            if (myGlobal.targetSplited == None):
                myGlobal.targetSplited = {component + '&' + serverType: targetSplited}
            else:
                myGlobal.targetSplited[component + '&' + serverType] = targetSplited
        else:
            RedisUtil().set_single_data(component + '&' + serverType, pickle.dumps(targetSplited))
