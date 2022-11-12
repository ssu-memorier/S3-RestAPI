import io
import json
from pathlib import Path

import jwt
import hashlib


def convertContents(contents):
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


def token2hash(token):
    decoded = jwt.decode(token, options={"verify_signature": False})

    email = decoded['email']
    provider = decoded['provider']

    return hashlib.sha256((provider+'/'+email).encode()).hexdigest()
