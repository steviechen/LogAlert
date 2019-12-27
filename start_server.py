#!/usr/bin/python
# -*- coding: utf-8 -*-
from flask import Flask,jsonify
from distutils.util import strtobool
from src.main.utils import ConfigurationUtil
from src.main.handler.LogExTrainHandler import LogExTrainHandler
from src.main.handler.LogExSaveModelHandler import LogExSaveModelHandler
from src.main.handler.LogExLoadModelHandler import LogExLoadModelHandler
from src.main.handler.LogExLoadTargetTrackingIdsHandler import LogExLoadTargetTrackingIdsHandler
from src.main.handler.LogExLoadRawDataHandler import LogExLoadRawDataHandler
from src.main.handler.LogExPredictBySingleHandler import LogExPredictBySingleHandler
from src.main.handler.LogExPredictByBatchHandler import LogExPredictByBatchHandler
from src.main.handler.LogExPredictFeedbackHandler import LogExPredictFeedbackHandler
from src.main.handler.LogExLoadConfigHandler import LogExLoadConfigHandler
from src.main.handler.LogExQueryConfigHandler import LogExQueryConfigHandler
from src.main.handler.LogExQueryTargetTrackingIdHandler import LogExQueryTargetTrackingIdHandler

settings = {
    'host': str(ConfigurationUtil.get("System", "host")),
    'debug': strtobool(ConfigurationUtil.get("System", "debug_mode")),
    'port': int(ConfigurationUtil.get("System", "port"))
}

app = Flask(__name__)

@app.route('/load/Logex/config', methods=['POST'])
def loadConfig(): return jsonify(LogExLoadConfigHandler().post())

@app.route('/load/Logex/model', methods=['POST','GET'])
def loadModel(): return jsonify(LogExLoadModelHandler().postOrGet())

@app.route('/load/Logex/targetTrackingIds', methods=['POST','GET'])
def loadTargetTrackingIds(): return jsonify(LogExLoadTargetTrackingIdsHandler().postOrGet())

@app.route('/load/Logex/rawData', methods=['POST'])
def loadRawData(): return jsonify(LogExLoadRawDataHandler().post())

@app.route('/predict/LogexByBatch', methods=['POST'])
def predictBatch(): return jsonify(LogExPredictByBatchHandler().post())

@app.route('/predict/Logex', methods=['POST'])
def predictSingle(): return jsonify(LogExPredictBySingleHandler().post())

@app.route('/predict/LogexFeedback', methods=['POST'])
def predictFeedback(): return jsonify(LogExPredictFeedbackHandler().post())

@app.route('/query/Logex/config', methods=['GET'])
def queryConfig(): return jsonify(LogExQueryConfigHandler().get())

@app.route('/query/Logex/targetTrackingId', methods=['GET'])
def queryTargetTrackingIds(): return jsonify(LogExQueryTargetTrackingIdHandler().get())

@app.route('/train/Logex', methods=['POST','GET'])
def trainModel(): return jsonify(LogExTrainHandler().postOrGet())

@app.route('/save/Logex/model', methods=['POST','GET'])
def saveModel(): return jsonify(LogExSaveModelHandler().postOrGet())

if __name__ == "__main__":
    app.run(host=settings['host'], port=settings['port'], debug=settings['debug'])
