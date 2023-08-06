import time
import sys
import requests
import json
from flask import Flask, request

server = Flask(__name__)


@server.route('/wq', methods=['POST', 'GET'])
def _do():
    _echo(request.get_json())
    return 'ok'


class Webhook:
    def __init__(self, echo):
        self.myip = requests.get('https://api.ipify.org').text
        global _echo
        _echo = echo

    def register(self, s :requests.Session):
        self.r = s.request('PUT', 'https://edge.qiwi.com/payment-notifier/v1/hooks', params={
            'hookType': 1,
            'param': 'http://{0}/wq'.format(self.myip),
            'txnType': 0,
        })
        if self.r.status_code == 200:
            print('qiwi webhook ok')
        elif self.r.status_code == 422:
            print('qiwi webhook already created')
        server.run('0.0.0.0', port=80)
