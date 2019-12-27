import numpy as np
import pandas as pd
from collections import defaultdict
from src.main.domain.vo.DocList import DocList
from src.main.utils.LogExProcessUtil import LogExProcessUtil
from src.main.utils.LogExTrainUtil import LogExTrainUtil

class LogExPredictUtil(object):
    def __init__(self,rootPath,predictTag):
        self.rootPath = rootPath
        self.predictTag = predictTag
        self.logExProcessUtil = LogExProcessUtil(predictTag)
        self.logExTrainUtil = LogExTrainUtil(rootPath,predictTag)

    def genPredSplited(self,trackingIds,reqinterval='7d',rawDataTag = 'default'):
        self.logExTrainUtil.genFilterFileBytrackingIdsByMutiproc(trackingIds,reqinterval,rawDataTag=rawDataTag)
        return self.logExTrainUtil.genSplitedData()

    def getD2VDF(self,predD2VDocPath,d2vModel,predSplited):
        docListPred = DocList(predD2VDocPath)
        d2vModel.build_vocab(docListPred, update=True)
        for i in range(10):
            d2vModel.train(docListPred, total_examples=d2vModel.corpus_count, epochs=d2vModel.iter)
        return pd.DataFrame(np.array([d2vModel.docvecs[i] for i in range(predSplited.size)])),d2vModel

    def getW2VDF(self,predSplited,w2vModel):
        documents = predSplited
        predTexts = [[word for word in document.split(' ')] for document in documents]
        frequency = defaultdict(int)
        for predText in predTexts:
            for token in predText:
                frequency[token] += 1
        predTexts = [[token for token in predText if frequency[token] >= 5] for predText in predTexts]

        w2vModel.build_vocab(predTexts, update=True)
        w2vModel.train(predTexts, total_examples=w2vModel.corpus_count, epochs=w2vModel.iter)

        w2vFeat = np.zeros((len(predTexts), 300))
        w2vFeatAvg = np.zeros((len(predTexts), 300))
        i = 0
        for line in predTexts:
            num = 0
            for word in line:
                # print(word)
                num += 1
                vec = w2vModel[word]
                w2vFeat[i, :] += vec
            w2vFeatAvg[i, :] = w2vFeat[i, :] / num
            i += 1

        w2vFeatDF = pd.DataFrame(w2vFeat)
        w2vFeatAvgDF = pd.DataFrame(w2vFeatAvg)

        return w2vFeatDF,w2vFeatAvgDF,w2vModel

    def genPredDF(self,predSplited,d2vModel,w2vModel):
        self.logExTrainUtil.genTrainDataForD2V(predSplited)
        predD2VDocPath = self.rootPath + '/Logex/output/corpus/d2v_%s.txt'%(self.predictTag)
        d2vDF,d2vModel = self.getD2VDF(predD2VDocPath,d2vModel,predSplited)
        w2vFeatDF,w2vFeatAvgDF,w2vModel = self.getW2VDF(predSplited,w2vModel)
        predDF = pd.concat([d2vDF, w2vFeatDF, w2vFeatAvgDF], axis=1)
        predDF.set_index(predSplited.index)
        return predDF,d2vModel,w2vModel

    def genTargetDF(self,targetSplited,targetTag,d2vModel,w2vModel):
        targetD2vDocPath = self.rootPath+'/Logex/output/corpus/d2v_target_%s.txt'%(targetTag)
        d2vDF,d2vModel = self.getD2VDF(targetD2vDocPath,d2vModel,targetSplited)
        w2vFeatDF,w2vFeatAvgDF,w2vModel = self.getW2VDF(targetSplited,w2vModel)
        targetDF = pd.concat([d2vDF, w2vFeatDF, w2vFeatAvgDF], axis=1)
        targetDF.set_index(targetSplited.index)
        return targetDF,d2vModel,w2vModel

    def genRawData(self,rawCSVPath='defalutPath'):
        if(rawCSVPath == 'defalutPath'):rawCSVPath = self.rootPath+'/Logex/input/resFilter_%s.csv'%self.trainTag
        rawData = pd.read_csv(rawCSVPath)
        return rawData



