# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogAlertQueryTargetTrackingIdService import LogAlertQueryTargetTrackingIdService

class LogAlertQueryTargetTrackingIdHandler():
    def __init__(self):
        super().__init__()
        self.LogAlertQueryTargetTrackingIdService = LogAlertQueryTargetTrackingIdService()

    def get(self):
        component = request.args.get('component',type=str,default='all')
        serverType = request.args.get('serverType',type=str,default='all')
        return self.LogAlertQueryTargetTrackingIdService.make_procedure(component,serverType)