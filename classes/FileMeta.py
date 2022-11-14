from utils import converter, elements
from constants import REQUEST as RQ


class FileMeta:
    UID_LENGTH = 64
    DIR_LENGTH = 200
    KEY_LENGTH = 100

    def __init__(self, tokenData, keyDirData):
        decoded = converter.jwtTokenDecoder(
            tokenData[RQ.AUTHORIZATION])    # ['authorization']
        email = decoded['email']
        provider = decoded['provider']

        self.uid = elements.getUid(email, provider)
        self.dir = keyDirData[RQ.DIR]
        self.key = keyDirData[RQ.KEY]

    @property
    def data(self):
        return {
            RQ.UID: self.uid,
            RQ.DIR: self.dir,
            RQ.KEY: self.key
        }
