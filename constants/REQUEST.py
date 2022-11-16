SUCCESS = True
FAIL = False

# Request Key
UID = "uid"
KEY = "key"
DIR = 'dir'
DATA = "data"
TOKEN = 'token'

COOKIES_TOKEN = 'jwt'

AUTHORIZATION = 'Authorization'
CONTENTS = "contents"

# User Schema Max Length
UID_LENGTH = 64
DIR_LENGTH = 200
KEY_LENGTH = 100

# 임시 UID
TEST_UID = 'test_id'

# zip 파일 생성
ZIP = "application/zip"
CONTENT_DISPOSTION = 'Content-Disposition'
CONTENT_DISPOSTION_BODY = 'attachment; filename=data.zip'

LIMITED_FILESIZE = 20 * 1024 * 1024

# Http Method
GET, POST, PUT, DELETE = "GET", "POST", "PUT", "DELETE"

DEFAULT_JSON = {
    "editor": {
        "time": 0,
        "blocks": [
            {
                "id": '3W6kMa4BtB',
                "type": 'header',
                "data": {
                    "text": '',
                    "level": 2
                },
            },
        ],
        "version": '2.25.0',
    },
    "highlights": []
}

DEFAULT_OBJECT_LIST = [{'Key': ""}]
