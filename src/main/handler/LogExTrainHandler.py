# -*- coding: utf-8 -*-
from flask import request
from src.main.service.impl.LogAlertTrainService import LogAlertTrainService
from src.main.domain.vo.LogAlertTrain import LogAlertTrain
from src.main.domain.vo.Message import Message

class LogAlertTrainHandler():
    def __init__(self):
        super().__init__()
        self.LogAlertTrainService = LogAlertTrainService()

    def postOrGet(self):
        if request.method == "POST":
            body = request.get_json()
            trainFiles = []
            for tainFile in list(body.get('trainfiles', [])):
                trainFiles.append(LogAlertTrain(tainFile['tag'], tainFile['component'], tainFile['servertype'], tainFile['path']))
            self.LogAlertTrainService.make_procedure_post(trainFiles)
            return Message("train finished !").__dict__
        else:
            trainSize = request.args.get('trainSize',type=str,default='7')
            self.LogAlertTrainService.make_procedure_request(trainSize)
            return Message("train finished !").__dict__


