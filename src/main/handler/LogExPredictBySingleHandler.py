# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogAlertPredictSingleService import LogAlertPredictSingleService
from src.main.domain.vo.LogAlertTrackingId import LogAlertTrackingId,Desc

class LogAlertPredictBySingleHandler():
    def __init__(self):
        super().__init__()
        self.LogAlertPredictSingleService = LogAlertPredictSingleService()

    def post(self):
        body = request.get_json()
        trackingId = LogAlertTrackingId(body['name'],'',Desc(body['desc']['component'],body['desc']['servertype'],body['desc']['dc']))
        return self.LogAlertPredictSingleService.make_procedure(trackingId)

