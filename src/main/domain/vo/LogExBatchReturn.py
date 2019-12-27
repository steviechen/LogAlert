from .LogExTrackingId import Desc
class LogExBatchReturn(object):
    def __init__(self,name,tag,desc,keyWords,distance):
        self.name = name
        self.tag = tag
        self.distance = distance
        self.keyWords = keyWords
        self.desc:Desc = desc
