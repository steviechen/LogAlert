#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask,jsonify
from distutils.util import strtobool
from src.main.utils import ConfigurationUtil
from src.main.handler.LogAlertTrainHandler import LogAlertTrainHandler
from src.main.handler.LogAlertSaveModelHandler import LogAlertSaveModelHandler
from src.main.handler.LogAlertLoadModelHandler import LogAlertLoadModelHandler
from src.main.handler.LogAlertLoadTargetTrackingIdsHandler import LogAlertLoadTargetTrackingIdsHandler
from src.main.handler.LogAlertLoadRawDataHandler import LogAlertLoadRawDataHandler
from src.main.handler.LogAlertPredictBySingleHandler import LogAlertPredictBySingleHandler
from src.main.handler.LogAlertPredictByBatchHandler import LogAlertPredictByBatchHandler
from src.main.handler.LogAlertPredictFeedbackHandler import LogAlertPredictFeedbackHandler
from src.main.handler.LogAlertLoadConfigHandler import LogAlertLoadConfigHandler
from src.main.handler.LogAlertQueryConfigHandler import LogAlertQueryConfigHandler
from src.main.handler.LogAlertQueryTargetTrackingIdHandler import LogAlertQueryTargetTrackingIdHandler

settings = {
    'host': str(ConfigurationUtil.get("System", "host")),
    'debug': strtobool(ConfigurationUtil.get("System", "debug_mode")),
    'port': int(ConfigurationUtil.get("System", "port"))
}

app = Flask(__name__)

@app.route('/load/LogAlert/config', methods=['POST'])
def loadConfig(): return jsonify(LogAlertLoadConfigHandler().post())

@app.route('/load/LogAlert/model', methods=['POST','GET'])
def loadModel(): return jsonify(LogAlertLoadModelHandler().postOrGet())

@app.route('/load/LogAlert/targetTrackingIds', methods=['POST','GET'])
def loadTargetTrackingIds(): return jsonify(LogAlertLoadTargetTrackingIdsHandler().postOrGet())

@app.route('/load/LogAlert/rawData', methods=['POST'])
def loadRawData(): return jsonify(LogAlertLoadRawDataHandler().post())

@app.route('/predict/LogAlertByBatch', methods=['POST'])
def predictBatch(): return jsonify(LogAlertPredictByBatchHandler().post())

@app.route('/predict/LogAlert', methods=['POST'])
def predictSingle(): return jsonify(LogAlertPredictBySingleHandler().post())

@app.route('/predict/LogAlertFeedback', methods=['POST'])
def predictFeedback(): return jsonify(LogAlertPredictFeedbackHandler().post())

@app.route('/query/LogAlert/config', methods=['GET'])
def queryConfig(): return jsonify(LogAlertQueryConfigHandler().get())

@app.route('/query/LogAlert/targetTrackingId', methods=['GET'])
def queryTargetTrackingIds(): return jsonify(LogAlertQueryTargetTrackingIdHandler().get())

@app.route('/train/LogAlert', methods=['POST','GET'])
def trainModel(): return jsonify(LogAlertTrainHandler().postOrGet())

@app.route('/save/LogAlert/model', methods=['POST','GET'])
def saveModel(): return jsonify(LogAlertSaveModelHandler().postOrGet())

if __name__ == "__main__":
    app.run(host=settings['host'], port=settings['port'], debug=settings['debug'])
