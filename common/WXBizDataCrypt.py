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
        sessionKey = base64.b64decode(self.sessionKey)
        encryptedData = base64.b64decode(encryptedData)
        iv = base64.b64decode(iv)
        cipher = AES.new(sessionKey, AES.MODE_CBC, iv)
        print('bbbbbbbbbbbbbbbbbbbbbbbbbbbbbbb'+str(cipher.decrypt(encryptedData)))
        decrypted = json.loads(self._unpad(cipher.decrypt(encryptedData)))
        if decrypted['watermark']['appid'] != self.appId:
            raise Exception('Invalid Buffer')

        return decrypted

    def _unpad(self, s):
        return s[:-ord(s[len(s) - 1:])]
