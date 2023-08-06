import os


class Config(object):
    ZK_NAMESPACE = os.environ.get('ZK_NAMESPACE', 'basic')
    ZK_HOSTS = os.environ.get('ZK_HOSTS', 'localhost:2181')
    SECRET_KEY = os.environ.get('SECRET_KEY', 'for_dev')
