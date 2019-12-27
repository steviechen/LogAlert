class LogExReturn(object):
    def __init__(self,matchRes,similarRes,predictDetail,targetDetails):
        self.matchRes = matchRes
        self.similarRes:list[SingleSimilarRes] = similarRes
        self.predictDetail = predictDetail
        self.targetDetails:list[TargetDetail] = targetDetails

class SingleSimilarRes(object):
    def __init__(self,trackingId,tag,distance,sort):
        self.sort = sort
        self.tag = tag
        self.trackingId = trackingId
        self.distance = distance

class PredictDetail(object):
    def __init__(self,trackingId,logs:list,keyWords):
        self.trackingId = trackingId
        self.keyWords = keyWords
        self.logs = logs

class TargetDetail(object):
    def __init__(self, trackingId,logs:list,keyWords):
        self.trackingId = trackingId
        self.keyWords = keyWords
        self.logs = logs



