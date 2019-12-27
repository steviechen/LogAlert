# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogAlertSaveModelService import LogAlertSaveModelService
from src.main.domain.vo.LogAlertModel import LogAlertModel

class LogAlertSaveModelHandler():
    def __init__(self):
        super().__init__()
        self.LogAlertSaveModelService = LogAlertSaveModelService()

    def postOrGet(self):
        if request.method == "POST":
            body = request.get_json()
            models = []
            for model in list(body.get('models',[])):
                models.append(LogAlertModel(model['component'],model['servertype'],model['path'],model['type']))
            return self.LogAlertSaveModelService.make_procedure(models)
        else:
            return self.LogAlertSaveModelService.make_procedure([])
