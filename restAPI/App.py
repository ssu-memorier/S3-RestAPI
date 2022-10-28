from utils.client import getClientBucket
from constant import KEY

# request 데이터를 가지고 있는 클래스


class App():
    def __init__(self, app):
        self.client, self.bucket = KEY.S3CLIENT, KEY.S3BUCKET
        [file, keyName, action] = app
        self.keyName = keyName
        self.file = file
        self.action = action
