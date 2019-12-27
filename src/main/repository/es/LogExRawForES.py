from elasticsearch import Elasticsearch
from src.main import myGlobal

class LogExRawForES:
    def __init__(self,dc,component):
        self.logExUrl = "https://%s:%s@clp%s-%s.webex.com/esapi"%(myGlobal.getConfigByName('es_user'),myGlobal.getConfigByName('es_password'),dc,component)
        self.index = "logs-*-%s-*"%(component)
        self.queryDay = myGlobal.getConfigByName('es_queryDay')
        self.es = Elasticsearch([self.logExUrl], verify_certs=False)

    def getExLogByTrackingId(self,trackingId,serverType,reqinterval='7d'):
        print("The processing trackingId is [%s]"%(trackingId))
        reqinterval = self.queryDay if int(self.queryDay[:-1]) >= int(reqinterval[:-1]) else reqinterval
        # queryStr = "\""+str(trackingId)+"\""+' AND type:'+str(serverType)
        queryStr = "\""+str(trackingId)+"\""
        req = {
                "version": "true",
                "sort": [
                      {
                          "@timestamp": {
                              "order": "desc",
                              "unmapped_type": "boolean"
                          }
                      }
                  ],
                "query": {
                    "bool": {
                        "must": [
                        {
                          "query_string": {
                            "query": queryStr,
                            "analyze_wildcard": "true",
                            "default_field": "*"
                          }
                        },
                        {
                          "range": {
                            "@timestamp": {
                              "gte": "now-"+reqinterval,
                              "lte": "now",
                              "format": "epoch_millis"
                            }
                          }
                        }
                      ],
                      "must_not": []
                    }
                  }
                }
        try:
            result = self.es.search(index=self.index, body=req, size=1000, scroll='15m', timeout='5m',request_timeout=10)
        except Exception as e:
            print("query es fail" + e)

        ret = result['hits']['hits']
        sid = result['_scroll_id']
        scroll_size = result['hits']['total']

        maxLogNum = len(ret)

        while scroll_size > 0 and maxLogNum < 2000:
            try:
                ret1 = self.es.scroll(scroll_id=sid, scroll='2m')
            except Exception as e:
                print("query es fail" + e)
            # Update the scroll ID
            sid = ret1['_scroll_id']
            # Get the number of results that we returned in the last scroll
            ret += ret1['hits']['hits']
            maxLogNum = len(ret)
            scroll_size = len(ret1['hits']['hits'])

        print("The logNum of [%s] is [%d]"%(trackingId,len(ret)))
        return ret[0:2000]


