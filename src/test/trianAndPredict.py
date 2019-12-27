from gensim.models.word2vec import Word2Vec
from gensim.models import Doc2Vec
from gensim.models import KeyedVectors
import numpy as np
import pandas as pd
import re
import codecs
import jieba
import jieba.analyse
import jieba.posseg
from sklearn.externals import joblib
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression

from sklearn.metrics import f1_score
from sklearn.model_selection import cross_val_score
from sklearn.model_selection import train_test_split
from sklearn.model_selection import StratifiedKFold
from sklearn.model_selection import StratifiedShuffleSplit
from sklearn.linear_model import LogisticRegression
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer

import subprocess
from collections import namedtuple

import datetime as dt
import os
# model = word2vec.load()

# KeyedVectors.load_word2vec_format()
import sys
# reload(sys)
# sys.setdefaultencoding('utf8')

import time

currdate = dt.datetime.now().strftime('%F')

def log(stri):
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
    print(str(now) + ' ' + str(stri))
rootPath = '~'

rawdata = pd.read_csv(rootPath + '/LogAlert/rawdata/res.csv')

############################ 定义分词函数 ############################
def split_word(text, stopwords):
    word_list = jieba.cut(text)
    start = True
    result = ''
    for word in word_list:
        word = word.strip()
        if word not in stopwords:
            if start:
                result = word
                start = False
            else:
                result += ' ' + word
    return result

############################ 加载停用词 ############################
stopwords = {}
for line in codecs.open(rootPath + '/LogAlert/rawdata/stop.txt', 'r', 'utf-8'):
# for line in codecs.open(rootPath + '/LogAlert/stop.txt'):
    stopwords[line.rstrip()] = 1

############################ 分词 ############################
cw = lambda x: split_word(x, stopwords)
splited = rawdata["log"].apply(cw)

SentimentDocument = namedtuple('SentimentDocument', 'words tags')

class Doc_list(object):
    def __init__(self, f):
        self.f = f
    def __iter__(self):
        for i,line in enumerate(codecs.open(self.f,encoding='utf8')):
            words = line.strip().split(' ')
            tags = [int(words[0][2:])]
            words = words[1:]
            yield SentimentDocument(words,tags)

splited.to_csv(rootPath + '/LogAlert/input/splited_all.csv', index=None, encoding='utf8')

############################ tfidf ############################
# import pickle as p
#
# vectorizer = CountVectorizer(decode_error="replace")
# tfidftransformer = TfidfTransformer()
# # 注意在训练的时候必须用vectorizer.fit_transform、tfidftransformer.fit_transform
# # 在预测的时候必须用vectorizer.transform、tfidftransformer.transform
# vec_train = vectorizer.fit_transform(splited)
# x_tfidf_sp = tfidftransformer.fit_transform(vec_train)
#
# # 保存经过fit的vectorizer 与 经过fit的tfidftransformer,预测时使用
# feature_path = rootPath + '/LogAlert/output/model/feature.pkl'
# with open(feature_path, 'wb') as fw:
#     p.dump(vectorizer.vocabulary_, fw)
#
# tfidftransformer_path = rootPath + '/LogAlert/output/model/tfidftransformer.pkl'
# with open(tfidftransformer_path, 'wb') as fw:
#     p.dump(tfidftransformer, fw)
#
#
# np.save(rootPath + '/LogAlert/svm_data/x_sp.npy', splited)
# np.save(rootPath + '/LogAlert/svm_data/x_tfidf.npy', x_tfidf_sp)

# In[13]:


############################ 准备数据 ############################
doc_f = codecs.open(rootPath + '/LogAlert/output/corpus/doc_for_d2v_12w.txt', 'w', encoding='utf8')
for i, contents in enumerate(splited):
    words = []
    for word in contents.split(' '):
        words.append(word)
    tags = [i]
    if i % 10000 == 0:
        log('iter = %d' % i)
    doc_f.write(u'_*{} {}\n'.format(i, ' '.join(words)))
doc_f.close()
log('Job Done.')


# In[14]:


############################ dbow d2v ############################
d2v = Doc2Vec(dm=0, size=300, negative=5, hs=0, min_count=3, window=30, sample=1e-5, workers=8, alpha=0.025, min_alpha=0.025)
doc_list = Doc_list(rootPath + '/LogAlert/output/corpus/doc_for_d2v_12w.txt')
d2v.build_vocab(doc_list)

# df_lb = y_tr

for i in range(10):
    log('pass: ' + str(i))
    doc_list = Doc_list(rootPath + '/LogAlert/output/corpus/doc_for_d2v_12w.txt')
    d2v.train(doc_list, total_examples=d2v.corpus_count, epochs=d2v.iter)
    X_d2v = np.array([d2v.docvecs[i] for i in range(splited.size)])
#     scores = cross_val_score(LogisticRegression(C=3), X_d2v, df_lb, cv=5)
#     log('dbow: ' + str(scores) + ' ' + str(np.mean(scores)))
d2v.save(rootPath + '/LogAlert/output/model/dbow_d2v_12w.model')
log('Save done!')


# In[15]:




# coding=utf-8
from collections import defaultdict

from gensim.models import Word2Vec

############################ w2v ############################
documents = splited
log('documents number %d' % len(documents))

texts = [[word for word in document.split(' ')] for document in documents]
frequency = defaultdict(int)
for text in texts:
    for token in text:
        frequency[token] += 1
texts = [[token for token in text if frequency[token] >= 5] for text in texts]

log('Train Model...')
w2v = Word2Vec(texts, size=300, window=5, iter=15, workers=12)
w2v.save(rootPath + '/LogAlert/output/model/w2v_12w.model')
log('Save done!')


# In[20]:


# coding=utf-8
from collections import defaultdict

from gensim.models import Word2Vec

############################ 加载数据 & 模型 ############################
# documents = splited
# texts = [[word for word in document.split(' ')] for document in documents]
# frequency = defaultdict(int)
# for text in texts:
#     for token in text:
#         frequency[token] += 1
# texts = [[token for token in text if frequency[token] >= 5] for text in texts]

# model = Word2Vec.load(rootPath + '/LogAlert/output/model/w2v_12w.model')
model = w2v

############################ w2v ############################
log('Start get w2v feat..')
w2v_feat = np.zeros((len(texts), 300))
w2v_feat_avg = np.zeros((len(texts), 300))
i = 0
for line in texts:
    num = 0
    for word in line:
        num += 1
        vec = model[word]
        w2v_feat[i, :] += vec
    w2v_feat_avg[i, :] = w2v_feat[i, :] / num
    i += 1
    if i % 1000 == 0:
        log(i)

df_w2v = pd.DataFrame(w2v_feat)
df_w2v.columns = ['w2v_' + str(i) for i in df_w2v.columns]
df_w2v.to_csv(rootPath + '/LogAlert/output/feature/w2v/w2v_12w.csv', encoding='utf8', index=None)
df_w2v_avg = pd.DataFrame(w2v_feat_avg)
df_w2v_avg.columns = ['w2v_avg_' + str(i) for i in df_w2v_avg.columns]
df_w2v_avg.to_csv(rootPath + '/LogAlert/output/feature/w2v/w2v_avg_12w.csv', encoding='utf8', index=None)

log('Save w2v and w2v_avg feat done!')

x_sp = np.array([d2v.docvecs[i] for i in range(splited.size)])
df = pd.concat([pd.DataFrame(x_sp), df_w2v_avg], axis=1)
df.set_index(splited.index)


df.shape