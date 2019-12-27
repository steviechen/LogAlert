# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogExPredictBatchService import LogExPredictBatchService
from src.main.domain.vo.LogExTrackingId import LogExTrackingId,Desc

class LogExPredictByBatchHandler():
    def __init__(self):
        super().__init__()
        self.LogExPredictBatchService = LogExPredictBatchService()

    def post(self):
        body = request.get_json()
        trackingIds = []
        for trackingId in list(body.get('trackingIds',[])):
            desc = Desc(trackingId['desc']['component'],trackingId['desc']['servertype'],trackingId['desc']['dc'])
            trackingIds.append(LogExTrackingId(trackingId['name'],trackingId.get('tag',''),desc))
        return self.LogExPredictBatchService.make_procedure(trackingIds)
