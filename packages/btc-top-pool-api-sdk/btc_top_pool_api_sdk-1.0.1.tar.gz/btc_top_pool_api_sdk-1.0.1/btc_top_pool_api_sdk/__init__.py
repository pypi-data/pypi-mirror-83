# -*- coding: utf-8 -*-
import hashlib
import hmac
import json
import random
import time

import jwt
import requests


def _get_random_num():
    return random.randint(1000000000, 9999999999)


class Client:
    def __init__(self, url, client_id, secret_key, secret_salt, expire_seconds=180):
        self.url = url
        self.client_id = client_id
        self.secret_key = secret_key
        self.secret_salt = secret_salt
        self.expire_seconds = expire_seconds

    def call_api(self, action, parameter):
        now_timestamp = int(time.time())

        # create jwt token
        rnd = _get_random_num()
        exp = now_timestamp + self.expire_seconds
        play_load = {'clientId': self.client_id, 'rnd': rnd, 'exp': exp}
        token = jwt.encode(play_load, self.secret_key)

        # create sign
        data = json.dumps(parameter)
        sign_nonce = str(_get_random_num())
        need_sign_content = '%s%d%s%s%s' % (action, now_timestamp, data, sign_nonce, self.secret_salt)
        sign = hmac.new(bytes(self.secret_key, 'ascii'), bytes(need_sign_content, 'ascii'), digestmod=hashlib.sha256).hexdigest()

        # send request
        resp = requests.post(
            url=self.url,
            headers={'Authorization': token, 'Cache-Control': 'no-cache'},
            json={
                'action': action,
                'at': now_timestamp,
                'data': data,
                'signNonce': sign_nonce,
                'sign': sign,
            }
        )
        resp.raise_for_status()
        return resp.json()
