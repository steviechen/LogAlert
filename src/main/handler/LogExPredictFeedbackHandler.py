# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogExPredictFeedbackService import LogExPredictFeedbackService
from src.main.domain.vo.LogExTrackingId import LogExTrackingId,Desc

class LogExPredictFeedbackHandler():
    def __init__(self):
        super().__init__()
        self.LogExPredictFeedbackService = LogExPredictFeedbackService()

    def post(self):
        trackingIds = []
        for trackingId in list(request.form.get('trackingIds',default=[])):
            desc = Desc(trackingId['desc']['component'], trackingId['desc']['servertype'], trackingId['desc']['dc'])
            trackingIds.append(LogExTrackingId(trackingId['name'], trackingId.get('tag', ''), desc))
        clusterNum = request.form.get('clusterNum', default='2')
        topN = request.form.get('topN', default='10')
        return self.LogExPredictFeedbackService.make_procedure(trackingIds,clusterNum,topN)
