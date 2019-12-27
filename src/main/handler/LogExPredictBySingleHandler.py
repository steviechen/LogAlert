# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogExPredictSingleService import LogExPredictSingleService
from src.main.domain.vo.LogExTrackingId import LogExTrackingId,Desc

class LogExPredictBySingleHandler():
    def __init__(self):
        super().__init__()
        self.logExPredictSingleService = LogExPredictSingleService()

    def post(self):
        body = request.get_json()
        trackingId = LogExTrackingId(body['name'],'',Desc(body['desc']['component'],body['desc']['servertype'],body['desc']['dc']))
        return self.logExPredictSingleService.make_procedure(trackingId)

