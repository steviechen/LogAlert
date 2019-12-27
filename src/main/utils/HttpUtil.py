from urllib import request
from src.main.domain.vo.LogAlertFeedBack import Feedback,SingleResult
import json

class HttpUtil(object):
    def post(self,json,url):
        print(url)
        print(json)
        headers = {'Content-Type': 'application/json'}
        req = request.Request(url=url, headers=headers, data= bytes(json,'utf-8'))
        response = request.urlopen(req)
        return response.read().decode('utf-8')