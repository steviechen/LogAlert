# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogExQueryTargetTrackingIdService import LogExQueryTargetTrackingIdService

class LogExQueryTargetTrackingIdHandler():
    def __init__(self):
        super().__init__()
        self.logExQueryTargetTrackingIdService = LogExQueryTargetTrackingIdService()

    def get(self):
        component = request.args.get('component',type=str,default='all')
        serverType = request.args.get('serverType',type=str,default='all')
        return self.logExQueryTargetTrackingIdService.make_procedure(component,serverType)