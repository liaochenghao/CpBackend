# -*- coding: utf-8 -*-
import base64
import json
from Crypto.Cipher import AES
from CpBackend.settings import WX_SMART_CONFIG


class WXBizDataCrypt:
    def __init__(self, sessionKey):
        self.appId = WX_SMART_CONFIG['appid']
        self.sessionKey = base64.b64decode(sessionKey)

    def decrypt(self, encryptedData, iv):
        # base64 decode
        encryptedData = base64.b64decode(encryptedData)
        sessionKey = base64.b64decode(self.sessionKey)
        iv = base64.b64decode(iv)
        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)
        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))
        print('------------------------------------------------------------')

        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')
        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]
