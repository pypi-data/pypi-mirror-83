# -*- coding: utf-8 -*-
import os
import urllib
import zlib
import urllib.parse
import urllib.error
from pprint import pprint

import mitmproxy
from mitmproxy import http
from mitmproxy import ctx
import base64
import json
from garbevents.settings import Settings as ST


class GetData:
    """
    A garbevents HTTP request class.
    """
    events_list = []

    @staticmethod
    def chunks(arr, n):
        return [arr[i:i + n] for i in range(0, len(arr), n)]

    def response(self, flow):
        if flow.request.url.startswith(ST.url):
            response = json.loads(flow.response.get_text())
            ctx.log.info(response)
            res = flow.response.set_text(json.dumps(ST.mock))
            ctx.log.info(res)
            ctx.log.info('modify success')

