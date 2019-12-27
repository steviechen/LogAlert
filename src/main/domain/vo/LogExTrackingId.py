class LogExTrackingId(object):
    def __init__(self,name,tag,desc):
        self.name = name
        self.tag = tag
        self.desc:Desc = desc

class Desc(object):
    def __init__(self,component,servertype,dc):
        self.component = component
        self.servertype = servertype
        self.dc = dc