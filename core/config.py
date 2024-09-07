import yaml
import os
from loguru import logger
import secrets
class Config:
    def __init__(self):
        self.c = self.load_config()
        self.mongo_host = self.c.get('mongo_db', {}).get('host')
        self.mongo_port = self.c.get('mongo_db', {}).get('port')
        self.mongo_username = self.c.get('mongo_db', {}).get('username')
        self.mongo_password = self.c.get('mongo_db', {}).get('password')
        self.mongo_db_name = self.c.get('mongo_db', {}).get('db_name')
        self.mongo_collection_name = self.c.get('mongo_db', {}).get('collection_name')
        self.web_host = self.c.get('web', {}).get('host')
        self.web_port = self.c.get('web', {}).get('port')
        self.openai_apikey = self.c.get('openai', {}).get('apikey')
        self.openai_model = self.c.get('openai', {}).get('model')
        self.openai_endpoint = self.c.get('openai', {}).get('endpoint',"https://api.openai.com/v1/")
        self.auth_key = self.c.get('auth', {}).get('key',None)
        self.auth_referer_whilelist = self.c.get('auth', {}).get('referer_whilelist')
    def load_config(self):
        try:
            with open(f'{os.getcwd()}/config/config.yml', 'r') as file:
                return yaml.safe_load(file)
        except Exception as e:
            print(f"加载配置文件失败: {e}")
            return {}