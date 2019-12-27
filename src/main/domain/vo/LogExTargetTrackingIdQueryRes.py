from src.main.domain.vo.LogExTrackingId import LogExTrackingId
class LogExTargetTrackingIdQueryRes(object):
    def __init__(self,component,servertype,trackingIds):
        self.component = component
        self.servertype = servertype
        self.trackingIds:list[LogExTrackingId] = trackingIds
