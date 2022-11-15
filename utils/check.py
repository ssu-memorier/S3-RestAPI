import re


def checkDuplicate(key, contents):
    files = []
    for content in contents:
        if content.endswith('pdf'):
            tokens = content.split('/')
            keyName = tokens[-1][:-4]
            files.append(keyName)

    mainpattern = re.compile(f'{key}')      # 같은 파일을 찾는 용도
    subPattern = re.compile(f'^{key} \((\d)\)$')    # 중복되는 파일을 찾는 용도

    fileList = []
    for file in files:
        print(file, keyName)
        if mainpattern.match(file):
            for f in files:
                if f == file:
                    continue
                if subPattern.match(f):
                    fileList.append(f)
                    print(subPattern.match(f))
            if not fileList:
                return f"{key} (1).pdf"
    else:   # 중복되는 파일이 없음
        return key
