from src.main.domain.vo.LogAlertTrackingId import LogAlertTrackingId
class LogAlertTargetTrackingIdQueryRes(object):
    def __init__(self,component,servertype,trackingIds):
        self.component = component
        self.servertype = servertype
        self.trackingIds:list[LogAlertTrackingId] = trackingIds
