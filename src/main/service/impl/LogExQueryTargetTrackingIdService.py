#!/usr/bin/env python
# -*- coding: utf-8 -*-
from src.main.service.TrainingService import TrainingService
from src.main.domain.vo.LogExTrackingId import LogExTrackingId,Desc
from src.main.domain.vo.Message import Message
from src.main.domain.vo.LogExTargetTrackingIdQueryRes import LogExTargetTrackingIdQueryRes
from src.main import myGlobal
import pandas as pd
import os

class LogExQueryTargetTrackingIdService(TrainingService):
    def __init__(self):
        super().__init__()
        self.rootPath = myGlobal.getConfigByName('LogEx_rootPath')

    def make_procedure(self,queryComponent,queryServerType):
        result = []
        targetDict = {}
        for resfile in os.listdir(self.rootPath + '/Logex/input'):
            if resfile.startswith('resFilter_target'):
                component = resfile.split('.')[0].split('&')[0].split('_')[2]
                serverType = resfile.split('.')[0].split('&')[1]
                resFilter = pd.read_csv(self.rootPath + '/Logex/input/resFilter_target_%s.csv' %(component+'&'+serverType))
                targetTrackingIds = []
                for name,group in resFilter.groupby(['id','tag']):
                    targetTrackingIds.append(LogExTrackingId(name[0],name[1],Desc(component,serverType,'').__dict__).__dict__)
                targetDict[component+'&'+serverType] = targetTrackingIds

        if queryComponent == 'all':
            for component_serverType in targetDict.keys():
                result.append(LogExTargetTrackingIdQueryRes(component_serverType.split('&')[0],component_serverType.split('&')[1],targetDict[component_serverType]).__dict__)
        else:
            if queryComponent+'&'+queryServerType in targetDict.keys():
                result.append(LogExTargetTrackingIdQueryRes(queryComponent,queryServerType,targetDict[queryComponent+'&'+queryServerType]).__dict__)
            else:
                return Message("can not find the targetTrackingIds info for %s "%(queryComponent+'&'+queryServerType)).__dict__

        return result


