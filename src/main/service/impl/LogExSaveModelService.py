#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pickle
from src.main.utils.RedisUtil import RedisUtil
from src.main.service.TrainingService import TrainingService
from src.main.utils.LogAlertProcessUtil import LogAlertProcessUtil
from src.main.domain.vo.Message import Message
from src.main import myGlobal
from src.main.utils import ConfigurationUtil

class LogAlertSaveModelService(TrainingService):
    def __init__(self):
        super().__init__()
        self.LogAlertProcessUtil = LogAlertProcessUtil()
        self.deployModel = ConfigurationUtil.get('LogAlert', 'deployMode')
        self.defaultModelDir = myGlobal.getConfigByName('LogAlert_rootPath')+'/LogAlert/output/model'

    def make_procedure(self,models):
        msg = ''
        if(models==[]):
            if (self.deployModel == 'local'):
                if len(myGlobal.d2vModel.keys()) == 0 :
                    msg +=' can not find the d2v model in memory!'
                else:
                    for modelName in myGlobal.d2vModel.keys():
                        myGlobal.d2vModel[modelName].save(self.LogAlertProcessUtil.deleteExistFile(self.defaultModelDir+'/%s.model'%(modelName)))
                if len(myGlobal.w2vModel.keys()) == 0 :
                    msg +=' can not find the w2v model in memory!'
                else:
                    for modelName in myGlobal.w2vModel.keys():
                        myGlobal.w2vModel[modelName].save(self.LogAlertProcessUtil.deleteExistFile(self.defaultModelDir+'/%s.model'%(modelName)))
            else:
                print(self.getAllModelNamesInRedis())
                modelNamesInRedis = self.getAllModelNamesInRedis()
                if len(modelNamesInRedis) == 0:
                    msg +=' can not find the model in redis!'
                else:
                    for modelName in modelNamesInRedis:
                        pickle.loads(RedisUtil().get_single_data(modelName)).save(self.LogAlertProcessUtil.deleteExistFile(self.defaultModelDir+'/%s.model'%(modelName)))
        else:
            for model in models:
                if (self.deployModel == 'local'):
                    if(model.type=='d2v'):
                        modelName = 'd2v_dbow_'+model.component+'&'+model.servertype
                        if not modelName in myGlobal.d2vModel.keys():
                            msg += ' can not find the %s.model in memory!' %(modelName)
                        else:
                            if model.path!='':
                                myGlobal.d2vModel[modelName].save(model.path)
                            else:
                                myGlobal.d2vModel[modelName].save(self.LogAlertProcessUtil.deleteExistFile(self.defaultModelDir + '/%s.model' % (modelName)))

                    if(model.type=='w2v'):
                        modelName = 'w2v_'+model.component+'&'+model.servertype
                        if not modelName in myGlobal.w2vModel.keys():
                            msg += ' can not find the %s.model in memory!' %(modelName)
                        else:
                            if model.path != '':
                                myGlobal.w2vModel[modelName].save(model.path)
                            else:
                                myGlobal.w2vModel[modelName].save(self.LogAlertProcessUtil.deleteExistFile(self.defaultModelDir + '/%s.model' % (modelName)))
                else:
                    if (model.type == 'd2v'):
                        modelName = 'd2v_dbow_' + model.component + '&' + model.servertype
                    else:
                        modelName = 'w2v_' + model.component + '&' + model.servertype

                    if not RedisUtil().get_single_data(modelName):
                        msg += ' can not find the %s.model in redis!' %(modelName)
                    else:
                        if model.path != '':
                            pickle.loads(RedisUtil().get_single_data(modelName)).save(model.path)
                        else:
                            pickle.loads(RedisUtil().get_single_data(modelName)).save(self.LogAlertProcessUtil.deleteExistFile(self.defaultModelDir + '/%s.model' % (modelName)))

        if msg == '':
            return Message("save model finished!").__dict__
        else:
            return Message(msg).__dict__


    def getAllModelNamesInRedis(self):
        res = []
        for key in RedisUtil().get_All_Keys():
            key = key.decode()
            if str(key).startswith('d2v_dbow_') or str(key).startswith('w2v_'):
                res.append(key)
        return res

