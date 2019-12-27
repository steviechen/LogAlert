#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
from src.main.utils.RedisUtil import RedisUtil
from src.main import myGlobal
from src.main.domain.vo.Message import Message
from src.main.service.TrainingService import TrainingService
from src.main.utils import ConfigurationUtil

class LogExLoadConfigService(TrainingService):
    def __init__(self):
        super().__init__()
        self.deployModel = str(ConfigurationUtil.get('LogEx','deployMode'))

    def make_procedure(self,config:dict,subType:str):
        if not config.keys(): return Message('please add config for %s!'%subType).__dict__
        resSuccessStr = ''

        if self.deployModel == 'local':
            if subType not in myGlobal.config.keys():
                configForSubType = {}
                for key in config.keys():
                    configForSubType[key] = config.get(key)
                    resSuccessStr = resSuccessStr + ' ' + key
                myGlobal.config[subType] = configForSubType
            else:
                configForSubType = myGlobal.config[subType]
                for key in config.keys():
                    configForSubType[key] = config.get(key)
                    resSuccessStr = resSuccessStr + ' ' + key
                myGlobal.config[subType] = configForSubType
        else:
            if not RedisUtil().keyExists(subType+'Config'):
                configForSubType = {}
                for key in config.keys():
                    configForSubType[key] = config.get(key)
                    resSuccessStr = resSuccessStr + ' ' + key
                RedisUtil().set_single_data(subType+'Config',pickle.dumps(configForSubType))
            else:
                configForSubType = pickle.loads(RedisUtil().get_single_data(subType+'Config'))
                for key in config.keys():
                    configForSubType[key] = config.get(key)
                    resSuccessStr = resSuccessStr + ' ' + key
                RedisUtil().set_single_data(subType + 'Config', pickle.dumps(configForSubType))

        return Message("load config %s succcess for %s! "%(resSuccessStr.split(),subType)).__dict__

