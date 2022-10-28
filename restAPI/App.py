from utils.client import getClientBucket
# request 데이터를 가지고 있는 클래스


class App():
    def __init__(self, app):
        self.client, self.bucket = getClientBucket()
        [file, keyName, action] = app
        self.keyName = keyName
        self.file = file
        self.action = action
