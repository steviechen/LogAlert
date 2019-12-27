# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogExLoadRawDataService import LogExLoadRawDataService
from src.main.domain.vo.LogExTrackingId import LogExTrackingId,Desc
from src.main.domain.vo.Message import Message

class LogExLoadRawDataHandler():
    def __init__(self):
        super().__init__()
        self.logExLoadRawDataService = LogExLoadRawDataService()

    def post(self):
        body = request.get_json()
        trackingIds = []
        for trackingId in list(body.get('trackingIds',[])):
            desc = Desc(trackingId['desc']['component'],trackingId['desc']['servertype'],trackingId['desc']['dc'])
            trackingIds.append(LogExTrackingId(trackingId['name'],trackingId.get('tag',''),desc))
        self.logExLoadRawDataService.make_procedure(trackingIds)
        return Message("load trackingIds finished !").__dict__
