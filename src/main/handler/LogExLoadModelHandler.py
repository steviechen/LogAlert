# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogExLoadModelService import LogExLoadModelService
from src.main.domain.vo.LogExModel import LogExModel
from src.main.domain.vo.Message import Message

class LogExLoadModelHandler():
    def __init__(self):
        super().__init__()
        self.logExLoadModelService = LogExLoadModelService()

    def postOrGet(self):
        if request.method == "POST":
            body = request.get_json()
            models = []
            for model in list(body.get('models',[])):
                models.append(LogExModel(model['component'],model['servertype'],model['path'],model['type']))
            self.logExLoadModelService.make_procedure(models)
        else:
            self.logExLoadModelService.make_procedure([])
        return Message("load model finished !").__dict__
