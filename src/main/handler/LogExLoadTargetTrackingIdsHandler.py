# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogExLoadTargetTrackingIdService import LogExLoadTargetTrackingIdService
from src.main.domain.vo.LogExTrackingId import LogExTrackingId,Desc
from src.main.domain.vo.Message import Message

class LogExLoadTargetTrackingIdsHandler():
    def __init__(self):
        super().__init__()
        self.logExLoadTargetTrackingIdService = LogExLoadTargetTrackingIdService()

    def postOrGet(self):
        if request.method == "POST":
            body = request.get_json()
            trackingIds = []
            for trackingId in list(body.get('trackingIds', [])):
                desc = Desc(trackingId['desc']['component'], trackingId['desc']['servertype'], trackingId['desc']['dc'])
                trackingIds.append(LogExTrackingId(trackingId['name'], trackingId.get('tag', ''), desc))
            processWay = body.get('processWay','load')
            self.logExLoadTargetTrackingIdService.make_procedure(trackingIds,processWay)
        else:
            self.logExLoadTargetTrackingIdService.make_procedure([],'load')
        return Message("load target trackingIds finished !").__dict__


