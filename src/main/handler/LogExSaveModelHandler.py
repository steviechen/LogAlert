# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogExSaveModelService import LogExSaveModelService
from src.main.domain.vo.LogExModel import LogExModel

class LogExSaveModelHandler():
    def __init__(self):
        super().__init__()
        self.logExSaveModelService = LogExSaveModelService()

    def postOrGet(self):
        if request.method == "POST":
            body = request.get_json()
            models = []
            for model in list(body.get('models',[])):
                models.append(LogExModel(model['component'],model['servertype'],model['path'],model['type']))
            return self.logExSaveModelService.make_procedure(models)
        else:
            return self.logExSaveModelService.make_procedure([])
