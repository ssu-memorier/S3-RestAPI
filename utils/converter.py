import io
import json
from pathlib import Path

import jwt


def contents2List(contents):
    keys = []
    # contents 파싱진행
    for content in contents:
        if content['Key'].endswith("pdf"):      # 문서파일은 최근 변경사항에 영향 없음
            continue

        if content['Key'].split('.')+"pdf" not in contents:     # 문서 파일이 존재하지 않음
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
    try:
        return jwt.decode(token, options={"verify_signature": False})
    except jwt.exceptions.DecodeError:
        return None
