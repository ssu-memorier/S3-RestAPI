from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework import status, viewsets
from zipfile import ZipFile

from .s3 import *
from .serializers import FileSerializer, ListSerializer

from constants import REQUEST as RQ
from .models import Content


class FileViewSet(viewsets.ModelViewSet):
    def retrieve(self, request):

        input_data = {RQ.UID: RQ.TEST_UID}
        input_data[RQ.KEY] = request.GET[RQ.KEY]
        input_data[RQ.DIR] = request.GET[RQ.DIR]

        fileSerializer = FileSerializer(data=input_data)

        if fileSerializer.is_valid(raise_exception=True):
            uid = fileSerializer.data[RQ.UID]
            dir = fileSerializer.data[RQ.DIR]
            key = fileSerializer.data[RQ.KEY]

            if not isObjectExist(uid, dir, key):    # DB에 데이터가 있는지 우선 확인
                return Response(status.HTTP_404_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

            filePath = converter.dir2path(uid, dir, key)
            pdfContent, jsonContent = getObject(filePath)

            if pdfContent is None or jsonContent is None:     # 가져온 파일이 없는경우
                return Response(status.HTTP_404_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

            # set response
            response = HttpResponse(
                content_type=RQ.ZIP, status=status.HTTP_200_OK)
            response[RQ.CONTENT_DISPOSTION] = RQ.CONTENT_DISPOSTION_BODY

            # add zipFile and datas
            zipObj = ZipFile(response, 'w')
            zipObj.writestr(f"{key}.pdf", pdfContent)
            zipObj.writestr(f"{key}.json", jsonContent)

            return response

        else:
            return Response(status.HTTP_400_BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        request.data[RQ.UID] = RQ.TEST_UID
        fileSerializer = FileSerializer(data=request.data)

        if fileSerializer.is_valid(raise_exception=True):

            uid = fileSerializer.validated_data[RQ.UID]
            dir = fileSerializer.validated_data[RQ.DIR]
            key = fileSerializer.validated_data[RQ.KEY]

            if isObjectExist(uid, dir, key):    # DB에 데이터가 있는지 우선 확인
                return Response(status.HTTP_403_FORBIDDEN, status=status.HTTP_403_FORBIDDEN)

            # S3 생성
            filePath = converter.dir2path(uid, dir, key)
            isCreated = createObject(filePath, request.data[RQ.DATA])

            if not isCreated:   # 생성이 되지 않은 경우
                return Response(status.HTTP_404_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

            fileSerializer.save()       # DB 생성
            return Response(status.HTTP_201_CREATED, status=status.HTTP_201_CREATED)

        else:
            return Response(status.HTTP_400_BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request):
        input_data = {RQ.UID: RQ.TEST_UID}
        input_data[RQ.KEY] = request.data[RQ.KEY]
        input_data[RQ.DIR] = request.data[RQ.DIR]

        fileSerializer = FileSerializer(data=input_data)

        if fileSerializer.is_valid(raise_exception=True):
            uid = fileSerializer.data[RQ.UID]
            dir = fileSerializer.data[RQ.DIR]
            key = fileSerializer.data[RQ.KEY]

            if not isObjectExist(uid, dir, key):    # DB에 데이터가 있는지 우선 확인
                return Response(status.HTTP_404_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

            # S3 삭제
            filePath = converter.dir2path(uid, dir, key)
            isDeleted = deleteObject(filePath)

            if not isDeleted:   # 삭제가 되지 않은 경우
                return Response(status.HTTP_404_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

            # DB 삭제
            content = Content.objects.get(uid=uid, dir=dir, key=key)
            content.delete()

            return Response(status.HTTP_200_OK, status=status.HTTP_200_OK)
        else:
            return Response(status.HTTP_400_BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request):
        input_data = {RQ.UID: RQ.TEST_UID}
        input_data[RQ.KEY] = request.data[RQ.KEY]
        input_data[RQ.DIR] = request.data[RQ.DIR]

        fileSerializer = FileSerializer(data=input_data)

        if fileSerializer.is_valid(raise_exception=True):
            uid = fileSerializer.data[RQ.UID]
            dir = fileSerializer.data[RQ.DIR]
            key = fileSerializer.data[RQ.KEY]

            if not isObjectExist(uid, dir, key):    # DB에 데이터가 있는지 우선 확인
                return Response(status.HTTP_404_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

            filePath = converter.dir2path(uid, dir, key)
            isUpdated = saveJson(filePath, request.data[RQ.DATA])

            if not isUpdated:   # 생성이 되지 않은 경우
                return Response(status.HTTP_404_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

            return Response(status.HTTP_201_CREATED, status=status.HTTP_201_CREATED)
        else:
            return Response(status.HTTP_400_BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)


class ListViewSet(viewsets.ModelViewSet):
    def list(self, _):
        # DB상 uid 정보가 없는 경우
        if not Content.objects.filter(uid=RQ.TEST_UID):
            return Response(status.HTTP_404_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        listSerializer = ListSerializer(data={RQ.UID: RQ.TEST_UID})

        if listSerializer.is_valid(raise_exception=True):
            uid = listSerializer.data[RQ.UID]
            contents = getList(uid)

            if contents is None:       # Content가 없으면
                return Response(status.HTTP_404_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

            return JsonResponse({RQ.UID: RQ.TEST_UID, RQ.CONTENTS: contents}, status=status.HTTP_200_OK)
        else:

            return Response(status.HTTP_400_BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)


def isObjectExist(uid, dir, key):
    try:
        Content.objects.get(uid=uid, dir=dir, key=key)
        return True
    except:
        return False
