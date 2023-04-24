import requests

"""This class is a wrapper class for requests"""
class Client:
    def __init__(self, timeout=10, headers=None, proxies=None):
        self.session = requests.Session()
        self.session.headers.update(headers or {})
        self.session.proxies.update(proxies or {})
        self.session.timeout = timeout

    def get(self, url, params=None, **kwargs):
        return self.session.get(url, params=params, **kwargs)

    def post(self, url, data=None, json=None, **kwargs):
        return self.session.post(url, data=data, json=json, **kwargs)

    def put(self, url, data=None, **kwargs):
        return self.session.put(url, data=data, **kwargs)

    def delete(self, url, **kwargs):
        return self.session.delete(url, **kwargs)
