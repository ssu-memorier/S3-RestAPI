from utils import elements
from constants import REQUEST as RQ


class FileMeta:
    UID_LENGTH = 64
    DIR_LENGTH = 200
    KEY_LENGTH = 100

    def __init__(self, jwtToken, keyDirData):
        self.uid = elements.getUid(jwtToken['email'], jwtToken['provider'])
        self.dir = keyDirData[RQ.DIR]
        self.key = keyDirData[RQ.KEY]

    @property
    def data(self):
        return {
            RQ.UID: self.uid,
            RQ.DIR: self.dir,
            RQ.KEY: self.key
        }
