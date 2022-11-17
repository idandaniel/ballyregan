from enum import Enum


APP_NAME = 'proxy-fetcher'


class OutputFormats(str, Enum):
    TABLE ='table'
    JSON = 'json'
