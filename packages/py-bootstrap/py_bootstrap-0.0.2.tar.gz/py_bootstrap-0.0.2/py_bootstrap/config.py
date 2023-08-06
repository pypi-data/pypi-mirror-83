import re
import threading
import time
from qg_tool.tool import get_host_ip
import json
from qg_eureka import EurekaClient
import random
from importlib import import_module
import traceback
import os
import inspect
import logging
import requests
import atexit
from .log import init_log

log = logging.getLogger('bootstrap')


def is_config(obj):
    try:
        json.dumps(obj)
        return True
    except:
        return False


config = {}
bootstrap = import_module('bootstrap')

for member in inspect.getmembers(bootstrap, is_config):
    config[member[0]] = member[1]


def init_arg(name, default):
    if config.get(name, None):
        pass
    else:
        config[name] = default
    return config[name]


profile = init_arg('profile', 'prod')
extra_profiles = init_arg('extra_profiles', 'logger')
if not re.search(r'(^|(?<=,))logger($|(?=,))', extra_profiles):
    extra_profiles = extra_profiles + ',logger'
    config.update(extra_profiles=extra_profiles)
ip = init_arg('ip', get_host_ip())
port = init_arg('port', 5000)

config_server_name = config['config_server_name']
app_name = config['app_name']
eureka_url = config['eureka_url']


eureka = EurekaClient(app_name=app_name, port=port, ip_addr=ip,
                      eureka_url=eureka_url)


config_app = eureka.get_app(config_server_name)
config_instances = config_app['application']['instance']
config_instance = random.choice(config_instances)
url = '{homepage}{app_name}-{profile}{extra_profiles}.json'.format(
    homepage=config_instance['homePageUrl'], app_name=app_name, profile=profile, extra_profiles=f',{extra_profiles}' if extra_profiles else '')

settings = requests.get(url).json()
config.update(settings)
with open('config.json', 'w', encoding='utf-8') as f:
    f.write(json.dumps(config, ensure_ascii=False,
                       indent=4, separators=(',', ':')))
print('加载配置成功')


def register_eureka():
    eureka.register()
    atexit.register(lambda: eureka.deregister())

    def heart():
        while True:
            time.sleep(config.get('eureka_heart', 20))
            try:
                eureka.renew()
                log.debug('eureka renew')
                continue
            except:
                print(f'连不上eureka: {eureka_url}')
                traceback.print_exc()
            break
        register_eureka()
    heart_thread = threading.Thread(target=heart)
    heart_thread.setDaemon(True)
    heart_thread.start()


def get_app_homepage(name, **kwargs):
    app = eureka.get_app(name)
    if not app:
        return None
    config_instances = app['application']['instance']
    config_instance = random.choice(config_instances)
    log.debug('调度服务 {} 地址 {}'.format(name, config_instance['homePageUrl']))
    return config_instance['homePageUrl']


init_log()
if config.get('register', False):
    register_eureka()
