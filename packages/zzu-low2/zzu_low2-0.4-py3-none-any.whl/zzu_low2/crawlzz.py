import requests
import time


def get_create_time(cls):
    creat_time = int(round(time.time() * 1000))
    return creat_time


class CrawlAPI(object):
    def add(self, a, b):
        return a + b

    @classmethod
    def sub(cls, a, b):
        return a - b
