import pickle
from src.main.utils.RedisUtil import RedisUtil
from multiprocessing import Manager
from src.main.utils import ConfigurationUtil

manager = Manager()
targetSplited = manager.dict()
d2vModel = manager.dict()
w2vModel = manager.dict()
config = manager.dict()

default = {}
# LogAlert
default['LogAlert_rootPath'] = str(ConfigurationUtil.get('LogAlert','rootPath'))
default['LogAlert_unknownDist'] = str(ConfigurationUtil.get('LogAlert','unknownDist'))
default['LogAlert_levenshteinWeight'] = str(ConfigurationUtil.get('LogAlert','levenshteinWeight'))
default['LogAlert_leastSpaceNumInKeyWord'] = str(ConfigurationUtil.get('LogAlert','leastSpaceNumInKeyWord'))
default['LogAlert_leastKeyWordLength'] = str(ConfigurationUtil.get('LogAlert','leastKeyWordLength'))
#FeedBack
default['FeedBack_url'] = str(ConfigurationUtil.get('FeedBack','url'))
default['FeedBack_sendOrNotSend'] = str(ConfigurationUtil.get('FeedBack','sendOrNotSend'))
default['FeedBack_saveUnKnown'] = str(ConfigurationUtil.get('FeedBack','saveUnKnown'))
#es
default['es_user'] = str(ConfigurationUtil.get('es','user'))
default['es_password'] = str(ConfigurationUtil.get('es','password'))
default['es_queryDay'] = str(ConfigurationUtil.get('es','queryDay'))
default['es_queryField'] = str(ConfigurationUtil.get('es','queryField'))

config['default'] = default

if str(ConfigurationUtil.get('LogAlert','deployMode')) != 'local':
    RedisUtil().set_single_data('defaultConfig',pickle.dumps(default))

def getConfigByName(configName,type = 'default'):
    if str(ConfigurationUtil.get('LogAlert', 'deployMode')) == 'local':
        if type in config.keys() and configName in config[type].keys():
            return config[type][configName]
        else:
            return config['default'][configName]
    else:
        if RedisUtil().keyExists(type+'Config') and configName in pickle.loads(RedisUtil().get_single_data(type+'Config')).keys():
            return pickle.loads(RedisUtil().get_single_data(type+'Config'))[configName]
        else:
            return pickle.loads(RedisUtil().get_single_data('defaultConfig'))[configName]


