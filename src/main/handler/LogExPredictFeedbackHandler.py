# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogAlertPredictFeedbackService import LogAlertPredictFeedbackService
from src.main.domain.vo.LogAlertTrackingId import LogAlertTrackingId,Desc

class LogAlertPredictFeedbackHandler():
    def __init__(self):
        super().__init__()
        self.LogAlertPredictFeedbackService = LogAlertPredictFeedbackService()

    def post(self):
        trackingIds = []
        for trackingId in list(request.form.get('trackingIds',default=[])):
            desc = Desc(trackingId['desc']['component'], trackingId['desc']['servertype'], trackingId['desc']['dc'])
            trackingIds.append(LogAlertTrackingId(trackingId['name'], trackingId.get('tag', ''), desc))
        clusterNum = request.form.get('clusterNum', default='2')
        topN = request.form.get('topN', default='10')
        return self.LogAlertPredictFeedbackService.make_procedure(trackingIds,clusterNum,topN)
