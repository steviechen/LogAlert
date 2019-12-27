#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import pickle
from src.main.service.TrainingService import TrainingService
from src.main.utils.RedisUtil import RedisUtil
from gensim.models.word2vec import Word2Vec
from gensim.models import Doc2Vec
from src.main import myGlobal
from src.main.utils import ConfigurationUtil

class LogExLoadModelService(TrainingService):
    def __init__(self):
        super().__init__()
        self.defaultModelDir = myGlobal.getConfigByName('LogEx_rootPath')+'/Logex/output/model'
        self.deployModel = str(ConfigurationUtil.get('LogEx','deployMode'))

    def make_procedure(self,models):
        if(models==[]):
            for model in os.listdir(self.defaultModelDir):
                if model.startswith('.'): continue
                if len(model.split('&')) == 3: continue
                print('processing modelFile is: '+ model)
                modelName = model.split('.')[0].split('&')[0]+'&'+model.split('.')[0].split('&')[1]
                modelType = model.split('.')[0].split('_')[0]
                modelPath = self.defaultModelDir+'/'+model
                self.loadModelByPath(modelType,modelName,modelPath)
        else:
            for model in models:
                modelName = 'd2v_dbow_'+model.component+'&'+model.servertype
                modelType = model.type
                modelPath = model.path
                self.loadModelByPath(modelType,modelName,modelPath)
        return

    def loadModelByPath(self,modelType,modelName,modelPath):
        if (modelType == 'd2v'):
            if (self.deployModel == 'local'):
                if (myGlobal.d2vModel == None):
                    myGlobal.d2vModel = {modelName: Doc2Vec.load(modelPath)}
                else:
                    myGlobal.d2vModel[modelName] = Doc2Vec.load(modelPath)
            else:
                RedisUtil().set_single_data(modelName, pickle.dumps(Doc2Vec.load(modelPath)))

        if (modelType == 'w2v'):
            if (self.deployModel == 'local'):
                if (myGlobal.w2vModel == None):
                    myGlobal.w2vModel = {modelName: Word2Vec.load(modelPath)}
                else:
                    myGlobal.w2vModel[modelName] = Word2Vec.load(modelPath)
            else:
                RedisUtil().set_single_data(modelName, pickle.dumps(Word2Vec.load(modelPath)))