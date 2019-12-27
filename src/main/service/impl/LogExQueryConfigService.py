#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
from src.main.utils.RedisUtil import RedisUtil
from src.main.service.TrainingService import TrainingService
from src.main.domain.vo.LogAlertConfig import LogAlertConfig
from src.main import myGlobal
from src.main.utils import ConfigurationUtil

class LogAlertQueryConfigService(TrainingService):
    def __init__(self):
        super().__init__()
        self.deployModel = ConfigurationUtil.get('LogAlert', 'deployMode')

    def make_procedure(self):
        config = {}
        if self.deployModel == 'local':
            for key in myGlobal.config.keys():
                config[key] = myGlobal.config.get(key)
        else:
            for key in self.getAllConfigNamesInRedis():
                config[key] = pickle.loads(RedisUtil().get_single_data(key))
        return LogAlertConfig(config).__dict__


    def getAllConfigNamesInRedis(self):
        res = []
        for key in RedisUtil().get_All_Keys():
            key = key.decode()
            if str(key).endswith('Config'):
                res.append(key)
        return res