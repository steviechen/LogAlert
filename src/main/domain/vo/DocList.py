import codecs
from collections import namedtuple

SentimentDocument = namedtuple('SentimentDocument', 'words tags')

class DocList(object):
    def __init__(self, f):
        self.f = f
    def __iter__(self):
        for i,line in enumerate(codecs.open(self.f,encoding='utf8')):
            words = line.strip().split(' ')
            tags = [int(words[0][2:])]
            words = words[1:]
            yield SentimentDocument(words,tags)