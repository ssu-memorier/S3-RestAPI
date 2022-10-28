from constant import REQUEST


def request(requestFile):
    file = requestFile[REQUEST.FILE]
    keyName = requestFile[REQUEST.KEYNAME]
    action = requestFile[REQUEST.ACTION]

    return [file, keyName, action]
