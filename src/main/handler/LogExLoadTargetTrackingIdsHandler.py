# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogAlertLoadTargetTrackingIdService import LogAlertLoadTargetTrackingIdService
from src.main.domain.vo.LogAlertTrackingId import LogAlertTrackingId,Desc
from src.main.domain.vo.Message import Message

class LogAlertLoadTargetTrackingIdsHandler():
    def __init__(self):
        super().__init__()
        self.LogAlertLoadTargetTrackingIdService = LogAlertLoadTargetTrackingIdService()

    def postOrGet(self):
        if request.method == "POST":
            body = request.get_json()
            trackingIds = []
            for trackingId in list(body.get('trackingIds', [])):
                desc = Desc(trackingId['desc']['component'], trackingId['desc']['servertype'], trackingId['desc']['dc'])
                trackingIds.append(LogAlertTrackingId(trackingId['name'], trackingId.get('tag', ''), desc))
            processWay = body.get('processWay','load')
            self.LogAlertLoadTargetTrackingIdService.make_procedure(trackingIds,processWay)
        else:
            self.LogAlertLoadTargetTrackingIdService.make_procedure([],'load')
        return Message("load target trackingIds finished !").__dict__


