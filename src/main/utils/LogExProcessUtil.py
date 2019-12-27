import os
import re
import pandas as pd
import numpy as np
import scipy
import socket
import gc
from src.main import myGlobal

class LogAlertProcessUtil(object):
    def __init__(self,processTag='default'):
        self.processTag = processTag
        self.stopFile = os.getcwd()+'/conf/stop.txt'
        self.commonWords = os.getcwd()+'/conf/commonWords.txt'
        self.keyWords = os.getcwd()+'/conf/keyWords.txt'
        self.errInfo = ['ERROR','Error','error','EXCEPTION','Exception','exception']

    def getHostName(self):
        return socket.gethostname().replace('_','-')

    def deleteExistFile(self,path):
        if(os.path.exists(path)):
            os.remove(path)
        return path

    def value_append(self,sr):
        ltemp = []
        for v in sr:
            ltemp.append(v)
        return ltemp

    def getErrLogAnchor(self,sizeList):
        print('The all log size is [%s]'%(sizeList))
        a = []
        for i in range(1,len(sizeList)-1):
            a.append([i-1,i,sizeList[i-1]-sizeList[i]])
        return pd.DataFrame(a,columns=["prefix","suffix","gap"]).sort_values("gap",ascending=False).reset_index(drop = True)['prefix'][0]+1

    def genProcessField(self, source):
        res = []
        for field in str(myGlobal.getConfigByName('es_queryField')).split(','):
            if field in source['_source'].keys():
                res.append(source['_source'][field])
        return '^'.join(res)

    def getImpLogsFromAll(self,logs,normLogSize=5):
        if(len(logs)==0): return []
        if(len(logs)==1): return logs
        resTmp = []
        for index, row in pd.DataFrame(logs).iterrows():
            processInfo = self.genProcessField(row)
            mesasgeSplit: list = self.splitWordSentence(processInfo)
            messageLen = len(mesasgeSplit.split(' '))
            resTmp.append([messageLen, processInfo])
        msgSizeAndLogDF = pd.DataFrame(resTmp,columns=['msgSize','log']).sort_values("msgSize",ascending=False).reset_index(drop=True)
        anchor = self.getErrLogAnchor(msgSizeAndLogDF['msgSize'].tolist())
        res = msgSizeAndLogDF['log'].tolist()[0:anchor+normLogSize]
        del msgSizeAndLogDF
        gc.collect()
        print('The Err msg anchor is [%s]'%(anchor))
        return res

    ###### 优化分词-Cosine ######
    def conc_list(self,ll):
        temp = ''
        for i in ll:
            temp = temp + i + ' '
        return temp.rstrip()

    def generate_words_from_file(self,file):
        with open(file, "r") as f:
            data = f.read().splitlines()
        return data

    def discard_comm_words(self,context, comm_words):
        arr = np.array(context)
        for i in comm_words:
            arr = arr[arr!= i]
            continue
        ll = arr.tolist()
        return [i for i in ll if i != '' and i != ' ']

    def splitWordSentence(self,x,resType='Str'):
        replacements = {
            "\'": " ",
            ",": " ",
            '"': ' ',
            "{": " ",
            "}": " ",
            "[": " ",
            "]": " ",
            "(": " ",
            ")": " ",
            "?": " ",
            "#": " ",
            ":": " ",
            "~": " ",
            "!": " ",
            "$": " ",
            ";": " ",
            "^": " ", # 已经将换行符转换成^,此处也应该将换行符切分
        }

        common_out = self.generate_words_from_file(self.commonWords)
        stn = x.translate(str.maketrans(replacements))
        temp_stn = re.sub('\\s+', ' ', stn.strip())
        ll = pd.Series(temp_stn.split(" "))
        ll = self.discard_comm_words(ll, common_out)
        if(resType == 'Str'): return self.conc_list([s for s in ll if not s.isdigit()])
        if(resType == 'List'): return [s for s in ll if not s.isdigit()]
    ###### 优化分词-Cosine ######

    ###### 分词-keyWords ######
    def replaceCommaAndLinebreak(self,string):
        string = string.replace('\\n','^')
        res = ""
        for i, ch in enumerate(string):
            if (ch == ',' and (string.find('[', i + 1) != -1 and string.find(']', i + 1) > string.find('[', i + 1) or string.find(']', i + 1) == -1)) :
                res += '^'
            elif (ch == ';' and (string.find('(', i + 1) != -1 and string.find(')', i + 1) > string.find('(', i + 1) or string.find(')', i + 1) == -1)):
                res += '^'
            else:
                res += ch

        return res

    def splitWordSentenceForKeyWords(self,x,resType='Str'):
        replacements = {
            '"':'',
            "{": "^",
            "}": "^",
        }
        # ";": "^",
        stn = x.translate(str.maketrans(replacements))
        temp_stn = re.sub('\\s+', ' ', stn.strip())
        ll = pd.Series(self.replaceCommaAndLinebreak(temp_stn).split("^")).apply(lambda x: x.replace('\\t','')).apply(lambda x: x.replace('\\',''))
        if(resType == 'Str'): return self.conc_list([s for s in ll if not s.isdigit()])
        if(resType == 'List'): return [s for s in ll if not s.isdigit()]

    def findKeywords(self,li):
        t = pd.Series(li)
        keywords = self.generate_words_from_file(self.keyWords)
        rs = []
        for index, word in enumerate(np.array(t)):
            if str(word).strip().startswith('at'):
                continue
            if len(str(word).split('.')):
                rs.append(word)
        for word in keywords:
            for i in t[t.map(lambda x: x.find(word) > -1)].values:
                rs.append(i)
        return rs

    def findUniqueKeywords(self,li):
        rs = pd.Series(np.unique(self.findKeywords(li))).apply(lambda x: x.strip()).tolist()
        l1 = sorted([word for word in rs if len(word.split(' ')) > int(myGlobal.getConfigByName('LogAlert_leastSpaceNumInKeyWord',self.processTag)) and len(word) > int(myGlobal.getConfigByName('LogAlert_leastKeyWordLength',self.processTag))],key=lambda word:len(str(word).split(' ')),reverse=True)
        return sorted(set(l1),key=l1.index)
    ###### 分词-keyWords ######

    ###### L-distance ######
    def simlarityCal(self,seq1, seq2):
        if len(seq2)>len(seq1):
            tmp = seq1
            seq1 = seq2
            seq2 = tmp
        num = 0
        for i in sorted(seq1, key=str.lower):
            allLDist = []
            for j in sorted(seq2, key=str.lower):
                split1 = self.splitWordSentenceForLevenshtein(i)
                split2 = self.splitWordSentenceForLevenshtein(j)
                allLDist.append(int(self.levenshtein(split1, split2)))
            minDist = min(allLDist)
            if minDist < 0.5 * max(len(split1), len(split2)):
                num = num + 1
        return -scipy.log(num / (len(seq1) + len(seq2))) * float(myGlobal.getConfigByName('LogAlert_levenshteinWeight',self.processTag))

    def levenshtein(self,seq1, seq2):
        size_x = len(seq1) + 1
        size_y = len(seq2) + 1
        matrix = np.zeros((size_x, size_y))
        for x in range(size_x):
            matrix[x, 0] = x
        for y in range(size_y):
            matrix[0, y] = y
        for x in range(1, size_x):
            for y in range(1, size_y):
                if seq1[x - 1] == seq2[y - 1]:
                    matrix[x, y] = min(
                        matrix[x - 1, y] + 1,
                        matrix[x - 1, y - 1],
                        matrix[x, y - 1] + 1
                    )
                else:
                    matrix[x, y] = min(
                        matrix[x - 1, y] + 1,
                        matrix[x - 1, y - 1] + 1,
                        matrix[x, y - 1] + 1
                    )
        return matrix[size_x - 1, size_y - 1]

    def splitWordSentenceForLevenshtein(self,x):
        replacements = {
            "\'": " ",
            ",": " ",
            '"': ' ',
            "{": " ",
            "}": " ",
            "[": " ",
            "]": " ",
            "(": " ",
            ")": " ",
            "?": " ",
            ":": " ",
            "~": " ",
            "!": " ",
            "$": " ",
            ";": " ",
        }
        stn = x.translate(str.maketrans(replacements))
        temp_stn = re.sub('\\s+', ' ', stn.strip())
        ll = pd.Series(temp_stn.split(" "))
        return [s for s in ll if not s.isdigit()]
    ###### L-distance ######
