import re


def checkDuplicate(key, contents):
    files = []
    for content in contents:
        if content.endswith('pdf'):
            tokens = content.split('/')
            keyName = tokens[-1][:-4]       # 파일 확장자 부분 잘라내기
            files.append(keyName)

    mainpattern = re.compile(f'{key}')      # 같은 파일을 찾는 용도
    subPattern = re.compile(f'^{key} \((\d)\)$')    # 중복되는 파일을 찾는 용도

    files.sort()
    fileList = []   # 같은 이름을 갖고 있는 파일 리스트
    for file in files:
        if mainpattern.match(file):
            for f in files:
                if f == file:
                    continue
                if subPattern.match(f):
                    fileList.append(f)
            if not fileList:
                return f"{key} (1)"
            else:
                break
    else:   # 중복되는 파일이 없음
        return key

    maxNum = 0
    for file in fileList:   # 같은 이름 파일 중 가장 마지막 번호를 구하기
        maxNum = max(maxNum, int(file.split("(")[-1][:-1]))

    return f"{key} ({maxNum+1})"
