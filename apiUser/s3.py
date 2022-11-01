from utils.client import getClientBucket

s3Client, s3Bucket = getClientBucket()      # 서버 클라이언트, 버킷 정보


def putObject(keyname, data):
    s3Client.upload_fileobj(data, s3Bucket, keyname)


def getObject(uid, keyname):
    contents = [data['Key'] for data in getList(uid)]
    try:
        # 해당 파일이 없는 경우 에러
        if keyname not in contents:
            raise KeyError
        return s3Client.get_object(
            Bucket=s3Bucket, Key=keyname)['Body'].read()
    except KeyError:
        return None


def deleteObject(uid, keyname):
    contents = [data['Key'] for data in getList(uid)]
    try:
        # 해당 파일이 없는 경우 에러
        if keyname not in contents:
            raise KeyError
        s3Client.delete_object(Bucket=s3Bucket, Key=keyname)

        return True
    except KeyError:
        return False


def getList(userId):
    try:
        return s3Client.list_objects_v2(Bucket=s3Bucket, Prefix=userId)[
            'Contents']       # 해당 userID를 가진 컨텐츠만 가져옴
    except KeyError:
        return None
