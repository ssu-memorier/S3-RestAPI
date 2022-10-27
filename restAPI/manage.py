from utils import log, test
from constant import REQUEST
from .App import App
from .serializers import request
from .post import *


def app(requestFile):
    data = App(request(requestFile))

    try:
        if data.action not in REQUEST.ACTION_LIST:
            raise TypeError(log.ActionError(data.action))

        if data.action == REQUEST.UPLOAD:
            upload(data)
        elif data.action == REQUEST.DOWNLOAD:
            obj = download(data)

            # 임시 테스트용 실행문
            if obj != None:
                test.getPdf(obj)

        elif data.action == REQUEST.DELETE:
            delete(data)
        elif data.action == REQUEST.GET_CONTENTS:
            getContents(data)

        log.printSuccessRest(data.action)

    except TypeError as err:
        print(err)
