# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogAlertLoadConfigService import LogAlertLoadConfigService

class LogAlertLoadConfigHandler():
    def __init__(self):
        super().__init__()
        self.LogAlertLoadConfigService = LogAlertLoadConfigService()

    def post(self):
        config = request.get_json().get("config",{})
        subType = request.get_json().get("subType",'default')
        res = self.LogAlertLoadConfigService.make_procedure(config,subType)
        return res
