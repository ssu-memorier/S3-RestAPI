from utils import converter
from constants import REQUEST
from constants import REQUEST as RQ

import hashlib


def getUid(jwtToken):
    decoded = converter.jwtTokenDecoder(jwtToken)
    email = decoded['email']
    provider = decoded['provider']

    newKeyword = provider+'/'+email
    return hashlib.sha256(newKeyword.encode()).hexdigest()


def getListObject(s3Client, s3Bucket, uid):  # 해당 userID를 가진 컨텐츠만 가져옴
    try:
        return s3Client.list_objects_v2(Bucket=s3Bucket, Prefix=uid)['Contents']
    except KeyError:
        return REQUEST.DEFAULT_OBJECT_LIST


def getContents(listObject):
    return [data['Key'] for data in listObject]


def getSerializerInputData(tokenData, keyDirData):
    uid = getUid(tokenData[RQ.TOKEN])

    input_data = {RQ.UID: uid}
    input_data[RQ.KEY] = keyDirData[RQ.KEY]
    input_data[RQ.DIR] = keyDirData[RQ.DIR]

    return input_data
