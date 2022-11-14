import io
import json
from pathlib import Path

import jwt

from constants import REQUEST as RQ


def contents2List(contents):
    keys = []
    # contents 파싱진행
    for content in contents:
        if content['Key'].split('.')[-1] != "pdf":
            continue

        tokens = content['Key'].split('/')
        dir, key = '/'.join(tokens[1:-1]), tokens[-1]

        lastModified = content["LastModified"]
        size = content["Size"]

        keyName = '.'.join(key.split('.')[:-1])

        keys.append({
            "key": keyName,
            "dir": dir,
            "lastModified": lastModified,
            "size": size
        })

    return keys


def str2byteIO(content):
    # string -> bytes -> byteIO
    return io.BytesIO(json.dumps(content).encode('utf-8'))


def dir2path(uid, dir, file):
    return str(Path(uid) / dir / file).replace('\\', '/')


def jwtTokenDecoder(token):
    return jwt.decode(token, options={"verify_signature": False})
