from urllib import request
from src.main.domain.vo.LogExFeedBack import Feedback,SingleResult
import json

class HttpUtil(object):
    def post(self,json,url):
        print(url)
        print(json)
        headers = {'Content-Type': 'application/json'}
        req = request.Request(url=url, headers=headers, data= bytes(json,'utf-8'))
        response = request.urlopen(req)
        return response.read().decode('utf-8')

if __name__ == '__main__':
    feedback = []
    feedback.append(SingleResult('meeting', 'mngsvr', 'csrf_token_in_post_header_is_not_valid2','1F4556395C3342A2B92A36432E170C18_1567166552092','F8395503640E4347B4044AB5E7A4E158_1567623414915').__dict__)
    res = HttpUtil().post(json=json.dumps(Feedback(feedback).__dict__),url='http://10.224.166.75:80/api/feedback/save')
    print(res)