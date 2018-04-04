# -*- coding: utf-8 -*-
import base64
import json
from Crypto.Cipher import AES
from CpBackend.settings import WX_SMART_CONFIG


class WXBizDataCrypt:
    def __init__(self, sessionKey):
        self.appId = WX_SMART_CONFIG['appid']
        self.sessionKey = sessionKey

    def decrypt(self, encryptedData, iv):
        # base64 decode
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)
        cipher = AES.new(self.sessionKey, AES.MODE_CBC, iv)
        data = self._unpad(cipher.decrypt(encryptedData))
        print('------------------------------------------------------------')
        print(data)
        decrypted = json.loads(data)
        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')
        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]
