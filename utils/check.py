from utils.elements import getPdfFileNames
import re

from constants import S3


def checkDuplicate(key, contents):
    files = getPdfFileNames(contents)
    fileName = key

    for k, v in S3.SPECIAL_REGEX.items():
        fileName = fileName.replace(k, v)
    mainpattern = re.compile(f'{fileName}')      # 같은 파일을 찾는 용도
    subPattern = re.compile(f'{fileName} \((\d)\)$')    # 중복되는 파일을 찾는 용도

    files.sort()
    duplicatedFileList = []   # 같은 이름을 갖고 있는 파일 리스트
    for file in files:
        # 파일명이 같은 경우 -> 다른 이름으로 저장해야함
        if mainpattern.match(file):
            # 파일명이 같지 않으면서 '파일명 (숫자)' 형식을 가진 파일명만 추출
            duplicatedFileList = [
                f for f in files if f != file and subPattern.match(f)]

            if duplicatedFileList:
                break    # '파일명 (숫자)' 형식의 파일이 있는 경우, 다음 스텝으로 진행

            # '파일명 (숫자)' 형식의 파일이 없는 경우 -> 파일명 (1)로 생성
            return f"{key} (1)"
    else:   # 중복되는 파일이 없음 -> 새로 생성하면 됨
        return key

    maxNum = 0
    for file in duplicatedFileList:   # 같은 이름 파일 중 가장 마지막 번호를 구하기
        maxNum = max(maxNum, int(file.split("(")[-1][:-1]))

    return f"{key} ({maxNum+1})"
