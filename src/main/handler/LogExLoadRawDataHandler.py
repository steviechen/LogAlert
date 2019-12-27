# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogAlertLoadRawDataService import LogAlertLoadRawDataService
from src.main.domain.vo.LogAlertTrackingId import LogAlertTrackingId,Desc
from src.main.domain.vo.Message import Message

class LogAlertLoadRawDataHandler():
    def __init__(self):
        super().__init__()
        self.LogAlertLoadRawDataService = LogAlertLoadRawDataService()

    def post(self):
        body = request.get_json()
        trackingIds = []
        for trackingId in list(body.get('trackingIds',[])):
            desc = Desc(trackingId['desc']['component'],trackingId['desc']['servertype'],trackingId['desc']['dc'])
            trackingIds.append(LogAlertTrackingId(trackingId['name'],trackingId.get('tag',''),desc))
        self.LogAlertLoadRawDataService.make_procedure(trackingIds)
        return Message("load trackingIds finished !").__dict__
