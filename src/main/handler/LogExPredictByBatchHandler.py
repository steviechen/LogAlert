# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogAlertPredictBatchService import LogAlertPredictBatchService
from src.main.domain.vo.LogAlertTrackingId import LogAlertTrackingId,Desc

class LogAlertPredictByBatchHandler():
    def __init__(self):
        super().__init__()
        self.LogAlertPredictBatchService = LogAlertPredictBatchService()

    def post(self):
        body = request.get_json()
        trackingIds = []
        for trackingId in list(body.get('trackingIds',[])):
            desc = Desc(trackingId['desc']['component'],trackingId['desc']['servertype'],trackingId['desc']['dc'])
            trackingIds.append(LogAlertTrackingId(trackingId['name'],trackingId.get('tag',''),desc))
        return self.LogAlertPredictBatchService.make_procedure(trackingIds)
