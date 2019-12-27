- [ LogExRestful](#head1)
	- [ Save Models](#head2)
		- [ Reuqest](#head3)
		- [ Response](#head4)
		- [ Descriptions](#head5)
	- [ Load Models](#head6)
		- [ Reuqest](#head7)
		- [ Response](#head8)
		- [ Descriptions](#head9)
	- [ Load Target tracking_ids](#head10)
		- [ Loading Methods](#head11)
		- [ Reuqest](#head12)
		- [ Response](#head13)
		- [ Descriptions](#head14)
	- [ Append more tracking_ids for training](#head15)
		- [ Reuqest](#head16)
		- [ Response](#head17)
		- [ Descriptions](#head18)
	- [ Updating Config attributes](#head19)
		- [ Reuqest](#head20)
		- [ Response](#head21)
		- [ Descriptions](#head22)
	- [ Training(post)](#head23)
		- [ Reuqest](#head24)
		- [ Response](#head25)
		- [ Descriptions](#head26)
	- [ Training(get)](#head27)
		- [ Reuqest](#head28)
		- [ Response](#head29)
		- [ Descriptions](#head30)
	- [ Predict Single tracking_id](#head31)
		- [ Reuqest](#head32)
		- [ Response](#head33)
		- [ Descriptions](#head34)
	- [ Predict Batch tracking_ids](#head35)
		- [ Reuqest](#head36)
		- [ Response](#head37)
		- [ Descriptions](#head38)
	- [ Clustering for unknown tracking_ids](#head43)
		- [ Reuqest](#head44)
		- [ Response](#head45)
		- [ Descriptions](#head46)
	- [ Inquiry to config attributes](#head47)
		- [ Reuqest](#head48)
		- [ Response](#head49)
		- [ Descriptions](#head50)
	- [ Inquiry to current target tracking_ids](#head51)
		- [ Reuqest](#head52)
		- [ Response](#head53)
		- [ Descriptions](#head54)
# <span id="head1"> LogExRestful</span>

### <span id="head2"> Save Models</span>

#### <span id="head3"> Reuqest</span>

- Method: **POST/GET**
- URL: ```/save/Logex/model```
- Headers： Content-Type:application/json
- Body:
```
{
    "models":[
		{
			"component":"meeting",
			"servertype":"mcrsvr",
			"path":"/Users/lujunyao/PycharmProjects/Anomaly-Detection-Service/data/Logex/output/model/d2v_dbow_meeting&mcrsvr&test.model",
			"type":"d2v"
		},
		{
			"component":"meeting",
			"servertype":"mcrsvr",
			"path":"/Users/lujunyao/PycharmProjects/Anomaly-Detection-Service/data/Logex/output/model/w2v_meeting&mcrsvr&test.model",
			"type":"w2v"
		}
	]
}
```

#### <span id="head4"> Response</span>
- Body
```
{"message": "save model finished!"}
```
#### <span id="head5"> Description</span>

- request body中的参数用于指定存储指定component+serverType组合的type模型到Path路径下
- 若请求类型为GET并且request body为空，则会将服务器内存所有指定命名格式的模型直接存储到项目指定的rootPath+"/Logex/output/model/"目录下
- 保存的模型文件的命名格式为：d2v_dbow_component&serverType.model 以及 w2v_component&serverType.model

### <span id="head6"> Load Models</span>
#### <span id="head7"> Reuqest</span>

- Method: **POST/GET**
- URL: ```/load/Logex/model```
- Headers： Content-Type:application/json
- Body:
```
{
    "models":[
		{
			"component":"meeting",
			"servertype":"mcrsvr",
			"path":"/Users/lujunyao/PycharmProjects/Anomaly-Detection-Service/data/Logex/output/model/d2v_dbow_meeting&mcrsvr&test.model",
			"type":"d2v"
		},
		{
			"component":"meeting",
			"servertype":"mcrsvr",
			"path":"/Users/lujunyao/PycharmProjects/Anomaly-Detection-Service/data/Logex/output/model/w2v_meeting&mcrsvr&test.model",
			"type":"w2v"
		}
	]
}
```

#### <span id="head8"> Response</span>
- Body
```
{"message": "load model finished!"}
```
#### <span id="head9"> Description</span>

- request body中的参数用于指定存储指定component+serverType组合的type模型到Path路径下)
- 若请求类型为GET，request body为空，则会将项目指定的rootPath+"/Logex/output/model/"目录下所有保存的模型文件存储到内存中（一般用于服务器迁移或者重启）
被加载的模型文件的命名格式为：d2v_dbow_component&serverType.model 以及 w2v_component&serverType.model

### <span id="head10"> Load Target tracking_ids</span>

#### <span id="head11"> Loading Methods</span>

Three methods to maintain target tracking_ids：
- 整体替换掉指定component+serverType组合下的所有targetTrackingId
- 向某一component+serverType组合添加targetTrackingId
- 删除某一component+serverType组合下targetTrackingId

#### <span id="head12"> Reuqest</span>

- Method: **POST/GET**
- URL: ```/load/Logex/targetTrackingIds```
- Headers： Content-Type:application/json
- Body:
```
{
	"processWay":"load",
	"trackingIds":[
		{
			"name":"5EF3A04694B8402BA47142C3166EF921_1567662662298",
			"desc":{
				"component":"meeting",
				"servertype":"mngsvr",
				"dc":"sj"
				},
			"tag":"csrf_token_in_post_header_is_not_valid"
		},
		{
			"name":"F8395503640E4347B4044AB5E7A4E158_1567623414915",
			"desc":{
				"component":"meeting",
				"servertype":"mngsvr",
				"dc":"sj"
				},
			"tag":"csrf_token_in_post_header_is_not_valid2"
		},		
		{
			"name":"D74238E3986645A4B6C1007E5C20D3C4_1567622717544",
			"desc":{
				"component":"meeting",
				"servertype":"mngsvr",
				"dc":"sj"
				},
			"tag":"Failed_to_convert"
		},
		{
			"name":"209E916225AB45B1B29E32B213A8053C_1567621773770",
			"desc":{
				"component":"meeting",
				"servertype":"mngsvr",
				"dc":"sj"
				},
			"tag":"delete_meeting_fail"
		}
	]
}
```

#### <span id="head13"> Response</span>
- Body
```
{"message": "load target trackingIds finished !"}
```
#### <span id="head14"> Description</span>

- 若请求类型为GET并且request body为空，则会将项目指定的rootPath+"/Logex/output/model/"目录下所有保存的targetTrackingId加载到内存中（一般用于服务器迁移或者重启）

### <span id="head15"> Append more tracking_ids for training</span>

#### <span id="head16"> Reuqest</span>

- Method: **POST**
- URL: ```/load/Logex/rawData```
- Headers： Content-Type:application/json
- Body:
```
{
	"trackingIds":[
		{
			"name":"5EF3A04694B8402BA47142C3166EF921_1567662662298",
			"desc":{
				"component":"meeting",
				"servertype":"mngsvr",
				"dc":"sj"
				},
			"tag":""
		},
		{
			"name":"F8395503640E4347B4044AB5E7A4E158_1567623414915",
			"desc":{
				"component":"meeting",
				"servertype":"mngsvr",
				"dc":"sj"
				},
			"tag":""
		},		
		{
			"name":"D74238E3986645A4B6C1007E5C20D3C4_1567622717544",
			"desc":{
				"component":"meeting",
				"servertype":"mngsvr",
				"dc":"sj"
				},
			"tag":""
		},
		{
			"name":"209E916225AB45B1B29E32B213A8053C_1567621773770",
			"desc":{
				"component":"meeting",
				"servertype":"mngsvr",
				"dc":"sj"
				},
			"tag":""
		}
	]
}
```

#### <span id="head17"> Response</span>
- Body
```
{"message": "load trackingIds finished !"}
```
#### <span id="head18"> Description</span>

- 该接口用于接受训练数据，将每天接受的trackingId按照component+serverType的组合生成不同的csv文件放到rootPath+"/Logex/rawdata/YYYY-MM-dd"文件夹下

### <span id="head19"> Updating Config attributes </span>

#### <span id="head20"> Reuqest</span>

- Method: **POST**
- URL: ```/load/Logex/config```
- Headers： Content-Type:application/json
- Body:
```
{
	"config":{
			"LogEx_unknownDist" : "0.2",
			"LogEx_levenshteinWeight":"0.1"
			}
}
```

#### <span id="head21"> Response</span>
- Body
```
{"message": "load config ['LogEx_unknownDist','LogEx_levenshteinWeight'] succcess! and load config [] fail!"}
```
#### <span id="head22"> Description</span>

- 该接口用于在系统处于运行状态下实时改变系统中所用到的各项参数值，返回结果中会表明有哪些参数修改成功（若不存在则为空），哪些修改失败（若不存在则为空）

### <span id="head23"> Training(post)</span>

#### <span id="head24"> Reuqest</span>

- Method: **POST**
- URL: ```/train/Logex```
- Headers： Content-Type:application/json
- Body:
```
{
	"trainfiles":[
		{
			"tag":"test1",
			"component":"meeting",
			"servertype":"mcrsvr",
			"path":"/Users/lujunyao/PycharmProjects/Anomaly-Detection-Service/data/Logex/rawdata/trackingId_new.csv"
		},
		{
			"tag":"test2",
			"component":"meeting",
			"servertype":"mcrsvr",
			"path":"/Users/lujunyao/PycharmProjects/Anomaly-Detection-Service/data/Logex/rawdata/trackingId_new.csv"
		}
	]
}
```

#### <span id="head25"> Response</span>
- Body
```
{"message": "train finished !"}
```
#### <span id="head26"> Description</span>

- 该接口用于训练模型，需要提供固定格式的训练文件，然后指定component+serverType，以及任意标识符（用于唯一标定模型），训练出来的模型会在
内存中自动替换或者增加某一component+serverType组合的模型
- 通过该接口训练出的模型为：d2v_dbow_component&serverType&tag.model 以及 w2v_component&serverType&tag.model
- 该接口训练出来的模型，不能通过不带request body的"/load/Logex/model"接口直接载入内存

### <span id="head27"> Training(get)</span>

#### <span id="head28"> Reuqest</span>

- Method: **GET**
- URL: ```/train/Logex?trainSize=```
- Headers： Content-Type:application/json
- Body:
```
```

#### <span id="head29"> Response</span>
- Body
```
{"message": "train finished !"}
```
#### <span id="head30"> Description</span>

- 该接口同样是用于训练数据，不过训练数据是通过“/load/Logex/targetTrackingIds”接口提前存储到本地，因此只需要通过trainSize参数来指定
（表示从当前日期的前一天开始到前N天的数据，N=trainSize，默认值为7），训练出来的模型会在内存中自动替换或者增加某一component+serverType
组合的模型
- 通过该接口训练出的模型为：d2v_dbow_component&serverType.model 以及 w2v_component&serverType.model
（不带tag参数，与训练(post)接口训练出的模型进行区分）
- 该接口训练出来的模型，可以通过不带request body的加载模型接口直接载入内存

### <span id="head31"> Predict Single tracking_id</span>

#### <span id="head32"> Reuqest</span>

- Method: **POST**
- URL: ```/predict/Logex```
- Headers： Content-Type:application/json
- Body:
```
{
	"name":"000F87BC732947FA89F8D48606DD927F_1568654970040",
	"desc":{
		"component":"meeting",
		"servertype":"j2eeapp",
		"dc":"sj"
		}
}
```

#### <span id="head33"> Response</span>
- Body
```
对应trackingid所属的component+serverType缺少d2vModel：
{"message": "can not find the d2vModel for meeting&mcrsvr!"}
```
```
对应trackingid所属的component+serverType缺少w2vModel：
{"message": "can not find the w2vModel for meeting&mcrsvr!"}
```
```
对应trackingid所属的component+serverType缺少targetTrackingId：
{"message": "can not find the targetTrackingIds result for meeting&mcrsvr!"}
```
```
对应trackingid无法在es中查询到：（可能是由于网络紧张导致查询超时所造成或者是由于trackingid的生成时间超出的系统设置的查询时间范围，默认为7天）
{"message": "can not find the targetTrackingIds result for 000F87BC732947FA89F8D48606DD927F_1568654970040!"}
```
```
成功预测：内容较多，此处由于篇幅限制，故不做展示
```
#### <span id="head34"> Description</span>

- 该接口用于针对单一trackingId进行预测，将会返回所有该预测trackingId与其同一component+serverType组合下targetTrackingId的相似度比较结果，
以及所有trackingId的keywords信息及较为重要的原始log信息

### <span id="head35"> Predict batch tracking_ids</span>

#### <span id="head36"> Reuqest</span>

- Method: **POST**
- URL: ```/predict/LogexByBatch```
- Headers： Content-Type:application/json
- Body:
```
{
    "trackingIds":[
        {
            "name":"handleERROREvent-8df87aa8-35a3-4204-a30a-ad1ebd8d2ebb",
            "desc":{
                "component":"meeting",
                "servertype":"mcrsvr",
                "dc":"ta"
                },
            "tag":""
        },
        {
            "name":"dfe1e041-6004-4c88-9ede-b9b5683a7a47",
            "desc":{
                "component":"meeting",
                "servertype":"mcrsvr",
                "dc":"ta"
                },
            "tag":""
        },
        {
            "name":"f1f2ed97-c2f0-4903-a2c9-06b166cdcd67",
            "desc":{
                "component":"meeting",
                "servertype":"mcrsvr",
                "dc":"sj"
                },
            "tag":""
        }
    ]
}
```

#### <span id="head37"> Response</span>
- Body
```
[
    {
        "name": "handleERROREvent-8df87aa8-35a3-4204-a30a-ad1ebd8d2ebb",
        "tag": "Unknown",
        "distance": 0.2975166219715608,
        "keyWords": [
            "please refer to following detail at bottom \norg.springframework.jdbc.BadSqlGrammarException",
            "c.c.w.s.c.e.ExceptionTrace - handleERROREvent-8df87aa8-35a3-4204-a30a-ad1ebd8d2ebb - Exception occured",
            "The system has internal error"
            ],
        "desc": {
            "component": "meeting",
            "servertype": "mcrsvr",
            "dc": "ta"
            }
    },
    {
        "name": "dfe1e041-6004-4c88-9ede-b9b5683a7a47",
        "tag": "Failed to convert value of type of String to Long",
        "distance": 0.2371346992726309,
        "keyWords": [],
        "desc": {
            "component": "meeting",
            "servertype": "mcrsvr",
            "dc": "ta"
            }
    },
    {
        "name": "f1f2ed97-c2f0-4903-a2c9-06b166cdcd67",
        "tag": "BadSqlGrammarException, maybe too long sql issue",
        "distance": 0.19770845483809016,
        "keyWords": [],
        "desc": {
            "component": "meeting",
            "servertype": "mcrsvr",
            "dc": "sj"
            }
    }
]
```
#### <span id="head38"> Description</span>

- 该接口用于批量对trackingId进行预测，批量返回最相近的targetTrackingId的tag值，以及相似度距离distance，同时根据距离值判断预测的
trackingId是否与所有targetTrackingId均不相似，若全都不相似，则返回的tag值为"Unknown"并将该判定为Unknown的trackingId的keyWords
信息返回。
- 若判断存在相似的targetTrackingId，则keyWords为空（节约存储资源）

### <span id="head43"> Clustering for unknown tracking_ids</span>

#### <span id="head44"> Reuqest</span>

- Method: **POST**
- URL: ```/predict/LogexFeedback```
- Headers： Content-Type:application/json
- Body:
```
{
	"clusterNum":"2",
	"TopN":"10",
    "trackingIds":[
        {
            "name":"handleERROREvent-8df87aa8-35a3-4204-a30a-ad1ebd8d2ebb",
            "desc":{
                "component":"meeting",
                "servertype":"mcrsvr",
                "dc":"ta"
                },
            "tag":""
        },
        {
            "name":"dfe1e041-6004-4c88-9ede-b9b5683a7a47",
            "desc":{
                "component":"meeting",
                "servertype":"mcrsvr",
                "dc":"ta"
                },
            "tag":""
        },
        {
            "name":"f1f2ed97-c2f0-4903-a2c9-06b166cdcd67",
            "desc":{
                "component":"meeting",
                "servertype":"mcrsvr",
                "dc":"sj"
                },
            "tag":""
        }
    ]
}
```

#### <span id="head45"> Response</span>
- Body
```
{
    "feedback": [
        {
            "component": "meeting",
            "serverType": "mcrsvr",
            "keyWords": [
                {
                    "topicNum": "1",
                    "keyWords": [
                        "String",
                        " false",
                        " true",
                        "AppTokenUtil.java",
                        " APP_ADDIN",
                        "INFO",
                        "FeignConfiguration.java",
                        "URI",
                        "getSiteSettings",
                        " - generate token with KM system success"
                    ]
                },
                {
                    "topicNum": "2",
                    "keyWords": [
                        "CalendarErrorEventRunner.java",
                        " trackErrorResponse exception com.cisco.webex.addin.service.common.exception.entity.WebexServiceHandlerException",
                        "calendarErrorHandlerTaskExecutor-3",
                        " getUserWebexProfile catch exception com.cisco.webex.addin.service.common.exception.entity.WebexServiceHandlerException",
                        " syncEventInfo eventId",
                        "ScheduledRunnable.java",
                        " at java.util.concurrent.ScheduledThreadPoolExecutor",
                        "ScheduledThreadPoolExecutor.java",
                        "WebExUserInfoHandler.java",
                        "WebExUserCredentialProcedure.java"
                    ]
                }
            ]
        }
    ]
}
```
#### <span id="head46"> Description</span>

- 该接口用于对所有输入的trackingId进行聚类分析，需要指定聚类的簇集数量clusterNum，以及每个簇集中较为中要的TopN个关键字信息

### <span id="head47">Inquiry to config attributes</span>

#### <span id="head48"> Reuqest</span>

- Method: **GET**
- URL: ```/query/Logex/config```
- Headers： Content-Type:application/json
- Body:
```
```

#### <span id="head49"> Response</span>
- Body
```
{
    "config": {
        "LogEx_rootPath": "/Users/lujunyao/PycharmProjects/Anomaly-Detection-Service/data",
        "LogEx_unknownDist": "0.04",
        "LogEx_levenshteinWeight": "0.05",
        "FeedBack_url": "http://10.224.166.75:80/api/feedback/save",
        "FeedBack_sendOrNotSend": "false",
        "FeedBack_saveUnKnown": "true",
        "es_user": "xxxx",
        "es_password": "xxxx",
        "es_queryDay": "10d"
    }
}
```
#### <span id="head50"> Description</span>

- 由于系统内存中的参数可以通过“/load/Logex/config”接口进行热改变，故提供接口对当前所有参数进行查询

### <span id="head51">Inquiry to current target tracking_ids</span>

#### <span id="head52"> Reuqest</span>

- Method: **GET**
- URL: ```/query/Logex/targetTrackingId?component=meeting&serverType=mcrsvr```
- Headers： Content-Type:application/json
- Body:
```
```

#### <span id="head53"> Response</span>
- Body
```
[
    {
        "component": "meeting",
        "servertype": "mcrsvr",
        "trackingIds": [
            {
                "name": "*** handle ERROR event:  02b506ae-ca03-4ec6-b75e-70e8923f0cf0",
                "tag": "ERROR add-in bad sql issue,  ORA-01795: maximum number of expressions in a list is 1000",
                "desc": {
                    "component": "meeting",
                    "servertype": "mcrsvr",
                    "dc": ""
                }
            },
            {
                "name": "*** handle ERROR event: 0b3e7b27-8617-425e-9f4d-aa615ff079dc",
                "tag": "BadSqlGrammarException, maybe too long sql issue",
                "desc": {
                    "component": "meeting",
                    "servertype": "mcrsvr",
                    "dc": ""
                }
            },
            {
                "name": "*** handle NEW notification 75DD9E1CB12E42D3BEA3805D06759EB3",
                "tag": "NEW add-in bad sql issue,  ORA-01795: maximum number of expressions in a list is 1000",
                "desc": {
                    "component": "meeting",
                    "servertype": "mcrsvr",
                    "dc": ""
                }
            },
            {
                "name": "3ab0410d-eeb1-437c-9faf-53c1cc7743c7",
                "tag": "Add-in Cannot found meeting uuid map information",
                "desc": {
                    "component": "meeting",
                    "servertype": "mcrsvr",
                    "dc": ""
                }
            },
            {
                "name": "5dd92f38-4942-4ede-9193-62be13a692ec",
                "tag": "Failed to convert value of type of String to Long",
                "desc": {
                    "component": "meeting",
                    "servertype": "mcrsvr",
                    "dc": ""
                }
            },
            {
                "name": "70012CD0AA48425A91FE859071515519_1569738530337",
                "tag": "writing data to the APR native socket issue, maybe restart server issue",
                "desc": {
                    "component": "meeting",
                    "servertype": "mcrsvr",
                    "dc": ""
                }
            },
            {
                "name": "b5d6dcd1-dd88-4873-bb32-f4dbc08202e9",
                "tag": "add-in of delete service issue, will be fixed next release",
                "desc": {
                    "component": "meeting",
                    "servertype": "mcrsvr",
                    "dc": ""
                }
            },
            {
                "name": "ccc_2936c675-7bf0-48b8-96e0-7c5517fa289c",
                "tag": "JDBC connection issue",
                "desc": {
                    "component": "meeting",
                    "servertype": "mcrsvr",
                    "dc": ""
                }
            },
            {
                "name": "e810612a-6d6a-40d6-aed8-c1fad8b83509",
                "tag": "Add-in  Failed to convert value of type String to Long",
                "desc": {
                    "component": "meeting",
                    "servertype": "mcrsvr",
                    "dc": ""
                }
            }
        ]
    }
]
```
#### <span id="head54"> Description</span>

- 查询时若不指定‘component’以及‘serverType’，则会返回所有component+serverType组合的targetTrackingId
