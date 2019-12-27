class LogExClusterReturn(object):
    def __init__(self,feedback):
        self.feedback:list[SingleResult] = feedback

class SingleResult(object):
    def __init__(self,component,serverType,Topics):
        self.component = component
        self.serverType = serverType
        self.keyWords = Topics

class Topic(object):
    def __init__(self,topicNum,keyWords):
        self.topicNum = topicNum
        self.keyWords:list[str] = keyWords