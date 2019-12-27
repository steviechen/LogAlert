#!/usr/bin/env python
# -*- coding: utf-8 -*-
import datetime
import pandas as pd
import os
from src.main.service.TrainingService import TrainingService
from src.main.utils.TimeUtil import Timeutil
from src.main import myGlobal

class LogAlertLoadRawDataService(TrainingService):
    def __init__(self):
        super().__init__()
        self.timeUtil = Timeutil()
        self.rootPath = myGlobal.getConfigByName('LogAlert_rootPath')

    def make_procedure(self,trackingIds):
        rawDataDirPath = self.rootPath+'/LogAlert/rawdata/'+ str(datetime.date.today())
        rawData = pd.DataFrame(columns=['name','component','servertype','dc'])

        if not os.path.exists(rawDataDirPath): os.mkdir(rawDataDirPath)

        for trackingId in trackingIds:
            rawData = rawData.append({'name':trackingId.name,'component':trackingId.desc.component,'servertype':trackingId.desc.servertype,'dc':trackingId.desc.dc},ignore_index=True)

        for name,group in rawData.groupby(['component','servertype']):
            rawDataFilePath = rawDataDirPath+'/trackingId_%s.csv'%(name[0]+'&'+name[1])
            if not os.path.exists(rawDataFilePath):
                pd.DataFrame(group, columns=['name','dc']).to_csv(rawDataFilePath, index=False)
            else:
                pd.DataFrame(group, columns=['name','dc']).to_csv(rawDataFilePath, mode='a', header=False, index=False)

        return
