# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogExLoadConfigService import LogExLoadConfigService

class LogExLoadConfigHandler():
    def __init__(self):
        super().__init__()
        self.logExLoadConfigService = LogExLoadConfigService()

    def post(self):
        config = request.get_json().get("config",{})
        subType = request.get_json().get("subType",'default')
        res = self.logExLoadConfigService.make_procedure(config,subType)
        return res
