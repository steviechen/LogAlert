# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogExTrainService import LogExTrainService
from src.main.domain.vo.LogExTrain import LogExTrain
from src.main.domain.vo.Message import Message

class LogExTrainHandler():
    def __init__(self):
        super().__init__()
        self.logExTrainService = LogExTrainService()

    def postOrGet(self):
        if request.method == "POST":
            body = request.get_json()
            trainFiles = []
            for tainFile in list(body.get('trainfiles', [])):
                trainFiles.append(LogExTrain(tainFile['tag'], tainFile['component'], tainFile['servertype'], tainFile['path']))
            self.logExTrainService.make_procedure_post(trainFiles)
            return Message("train finished !").__dict__
        else:
            trainSize = request.args.get('trainSize',type=str,default='7')
            self.logExTrainService.make_procedure_request(trainSize)
            return Message("train finished !").__dict__


