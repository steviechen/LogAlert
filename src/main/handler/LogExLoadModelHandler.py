# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogAlertLoadModelService import LogAlertLoadModelService
from src.main.domain.vo.LogAlertModel import LogAlertModel
from src.main.domain.vo.Message import Message

class LogAlertLoadModelHandler():
    def __init__(self):
        super().__init__()
        self.LogAlertLoadModelService = LogAlertLoadModelService()

    def postOrGet(self):
        if request.method == "POST":
            body = request.get_json()
            models = []
            for model in list(body.get('models',[])):
                models.append(LogAlertModel(model['component'],model['servertype'],model['path'],model['type']))
            self.LogAlertLoadModelService.make_procedure(models)
        else:
            self.LogAlertLoadModelService.make_procedure([])
        return Message("load model finished !").__dict__
