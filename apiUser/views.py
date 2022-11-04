from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework import status, viewsets

from .s3 import *
from .serializers import FileSerializer, ListSerializer

from constants import REQUEST as RQ


class FileViewSet(viewsets.ModelViewSet):
    def retrieve(self, _, uid, keyName):
        if not requestValidCheck(FileSerializer, {RQ.UID: uid, RQ.KEYNAME: keyName}):
            return Response(status.HTTP_400_BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)

        path = f"{uid}/{keyName}"
        content = getObject(uid, path)

        if content is None:     # 가져온 파일이 없는경우
            return Response(status.HTTP_404_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        return HttpResponse(content, content_type=RQ.PDF, status=status.HTTP_200_OK)

    def create(self, request, uid, keyName):
        if not requestValidCheck(FileSerializer, {RQ.UID: uid, RQ.KEYNAME: keyName}):
            return Response(status.HTTP_400_BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)

        path = f"{uid}/{keyName}"
        isCreated = createObject(uid, path, request.data[RQ.DATA])

        if not isCreated:   # 생성이 되지 않은 경우
            return Response(status.HTTP_404_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        return Response(status.HTTP_201_CREATED, status=status.HTTP_201_CREATED)

    def destroy(self, _, uid, keyName):
        if not requestValidCheck(FileSerializer, {RQ.UID: uid, RQ.KEYNAME: keyName}):
            return Response(status.HTTP_400_BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)

        path = f"{uid}/{keyName}"
        isDeleted = deleteObject(uid, path)

        if not isDeleted:   # 삭제가 되지 않은 경우
            return Response(status.HTTP_404_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        return Response(status.HTTP_200_OK, status=status.HTTP_200_OK)


class ListViewSet(viewsets.ModelViewSet):
    def list(self, _, uid):
        if not requestValidCheck(ListSerializer, {RQ.UID: uid}):
            return Response(status.HTTP_400_BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)

        contents = getList(uid)

        if contents is None:       # Content가 없으면
            return Response(status.HTTP_404_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        return JsonResponse({'uid': uid, RQ.CONTENTS: contents}, status=status.HTTP_200_OK)


def requestValidCheck(serializer, data):    # request가 valid한지 check
    return serializer(data=data).is_valid()
