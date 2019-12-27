import os
import re
import csv
import codecs
import pandas as pd
from itertools import chain
from gensim.models.word2vec import Word2Vec
from gensim.models import Doc2Vec
from collections import defaultdict
from multiprocessing import Process,Manager
from src.main.domain.vo.DocList import DocList
from src.main.repository.es.LogAlertRawForES import LogAlertRawForES
from src.main.utils.LogAlertProcessUtil import LogAlertProcessUtil
from src.main.domain.vo.LogAlertTrackingId import LogAlertTrackingId,Desc

class LogAlertTrainUtil(object):
    def __init__(self,rootPath,trainTag):
        self.rootPath = rootPath
        self.trainTag = trainTag
        self.LogAlertProcessUtil = LogAlertProcessUtil()

    def genFilterDataByTrackingIds(self,processName,returnDict,trackingIds,reqinterval='7d'):
        filterData = []
        for trackingId in trackingIds:
            rawLogs = []
            try:
                rawLogs = LogAlertRawForES(trackingId.desc.dc,trackingId.desc.component).getExLogByTrackingId(trackingId.name,trackingId.desc.servertype,reqinterval)
            except Exception as e:
                print(e)
            filterLogs = self.LogAlertProcessUtil.getImpLogsFromAll(rawLogs)

            for filterLog in filterLogs:
                #将换行符替换成“^”,后期需要按照^进行字段切分
                filterLog = re.sub(r"\n\t", "^", filterLog, 0)
                filterData.append([trackingId.name,filterLog.replace(trackingId.name,''),trackingId.tag,trackingId.desc.dc])
            returnDict[processName] = filterData

    def genFilterFileBytrackingIdsByMutiproc(self,trackingIds,reqinterval='7d',processNum = 10,rawDataTag = 'default'):
        if (rawDataTag == 'default'): rawDataTag = self.trainTag
        returnDict = Manager().dict()
        processNum = min([len(trackingIds),int(processNum)])
        division = len(trackingIds)/processNum
        trackingIdsForMutiproc =[trackingIds[round(division * i):round(division * (i + 1))] for i in range(processNum)]
        jobs = []
        for i in range(processNum):
            p = Process(target=self.genFilterDataByTrackingIds, args=(i,returnDict,trackingIdsForMutiproc[i],reqinterval))
            jobs.append(p)
            p.start()

        for proc in jobs:
            proc.join()

        filterData =list(chain(*returnDict.values()))
        pd.DataFrame(filterData,columns=['id','log','tag','dc']).to_csv(self.LogAlertProcessUtil.deleteExistFile(self.rootPath+'/LogAlert/input/resFilter_%s.csv'%rawDataTag))
        return

    def appendFilterFileBytrackingIdsByMutiproc(self,trackingIds,reqinterval='7d',processNum = 10,rawDataTag = 'default'):
        if (rawDataTag == 'default'): rawDataTag = self.trainTag
        returnDict = Manager().dict()
        processNum = min([len(trackingIds),int(processNum)])
        division = len(trackingIds)/processNum
        trackingIdsForMutiproc =[trackingIds[round(division * i):round(division * (i + 1))] for i in range(processNum)]
        jobs = []
        for i in range(processNum):
            p = Process(target=self.genFilterDataByTrackingIds, args=(i,returnDict,trackingIdsForMutiproc[i],reqinterval))
            jobs.append(p)
            p.start()

        for proc in jobs:
            proc.join()

        filterData =list(chain(*returnDict.values()))

        savePath = self.rootPath+'/LogAlert/input/resFilter_%s.csv'%rawDataTag
        if not os.path.exists(savePath):
            pd.DataFrame(filterData,columns=['id','log','tag','dc']).to_csv(savePath)
        else:
            pd.DataFrame(filterData, columns=['id','log','tag','dc']).to_csv(savePath, mode='a', header=False)
        return

    def getAllTrackingId(self,rawDataTag = 'default'):
        if (rawDataTag == 'default'): rawDataTag = self.trainTag
        resFilter = pd.read_csv(self.rootPath+'/LogAlert/input/resFilter_%s.csv'%rawDataTag)
        return resFilter['id'].unique().tolist()

    def deleteByTrackingId(self,trackingIds,rawDataTag = 'default'):
        if (rawDataTag == 'default'): rawDataTag = self.trainTag
        resFilter = pd.read_csv(self.rootPath + '/LogAlert/input/resFilter_%s.csv' % rawDataTag)
        for trackingId in trackingIds:
            resFilter = resFilter[resFilter.id!=trackingId.name]
        pd.DataFrame(resFilter,columns=['id','log','tag','dc']).to_csv(self.LogAlertProcessUtil.deleteExistFile(self.rootPath+'/LogAlert/input/resFilter_%s.csv'%rawDataTag))
        return

    def genFilterFileByFilePathOnMutiproc(self,component,servertype,filePath='defalutPath',reqinterval='7d',processNum =10,rawDataTag='default'):
        if (filePath == 'defalutPath'): filePath = self.rootPath + '/LogAlert/rawdata/trackingIds_%s.csv' % (self.trainTag)
        data = open(filePath, 'r')
        dataline = csv.reader(data)
        trackingIds = []
        for i in dataline:
            if dataline.line_num == 1:
                continue
            trackingIds.append(LogAlertTrackingId(i[0],'',Desc(component,servertype,i[1])))
        self.genFilterFileBytrackingIdsByMutiproc(trackingIds,reqinterval,processNum,rawDataTag)
        return

    def genSplitedData(self,rawCSVPath='defalutPath'):
        if(rawCSVPath == 'defalutPath'):rawCSVPath = self.rootPath+'/LogAlert/input/resFilter_%s.csv'%self.trainTag
        cw = lambda x: LogAlertProcessUtil().splitWordSentence(x)
        rawData = pd.read_csv(rawCSVPath).groupby("id").agg(self.LogAlertProcessUtil.value_append).reset_index()
        splited = rawData['log'].map(lambda x:str(x)).apply(cw)
        return splited

    def genRawData(self,rawCSVPath='defalutPath'):
        if(rawCSVPath == 'defalutPath'):rawCSVPath = self.rootPath+'/LogAlert/input/resFilter_%s.csv'%self.trainTag
        rawData = pd.read_csv(rawCSVPath).groupby("id",as_index=False).agg(self.LogAlertProcessUtil.value_append).reset_index()
        return rawData

    def genTrainDataForD2V(self, splited):
        doc_f = codecs.open(self.LogAlertProcessUtil.deleteExistFile(self.rootPath+'/LogAlert/output/corpus/d2v_%s.txt'%(self.trainTag)),'w', encoding='utf8')
        for i, contents in enumerate(splited):
            words = []
            for word in contents.split(' '):
                words.append(word)
            doc_f.write(u'_*{} {}\n'.format(i, ' '.join(words)))
        doc_f.close()
        return

    def genD2VModelByDBOW(self,docListPath='defaultPath'):
        if(docListPath=='defaultPath'):docListPath=self.rootPath+'/LogAlert/output/corpus/d2v_%s.txt'%(self.trainTag)
        docList = DocList(docListPath)
        d2v = Doc2Vec(dm=0, size=300, negative=5, hs=0, min_count=3, window=30, sample=1e-5, workers=8, alpha=0.025,min_alpha=0.025)
        d2v.build_vocab(docList)
        for i in range(10):
            d2v.train(docList, total_examples=d2v.corpus_count, epochs=d2v.iter)
        d2v.save(self.LogAlertProcessUtil.deleteExistFile(self.rootPath+'/LogAlert/output/model/d2v_dbow_%s.model'%(self.trainTag)))
        return d2v

    def genW2VModel(self,documents):
        texts = [[word for word in document.split(' ')] for document in documents]
        frequency = defaultdict(int)
        for text in texts:
            for token in text:
                frequency[token] += 1
        texts = [[token for token in text if frequency[token] >= 5] for text in texts]
        w2v = Word2Vec(texts, size=300, window=5, iter=15, workers=8)
        w2v.save(self.LogAlertProcessUtil.deleteExistFile(self.rootPath+'/LogAlert/output/model/w2v_%s.model'%(self.trainTag)))
        return w2v


