from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .s3 import *
from .serializers import FileSerializer, ListSerializer

from constants import REQUEST as RQ


@api_view([RQ.GET, RQ.POST, RQ.DELETE])
def s3Object(request, uid, keyName):
    fileSerializer = FileSerializer(data={RQ.UID: uid, RQ.KEYNAME: keyName})

    if not fileSerializer.is_valid():   # 적합하지 않는 코드의 경우
        return Response(status.HTTP_400_BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)

    path = f"{uid}/{keyName}"

    if request.method == RQ.POST:       # Post
        rqStatus = createObject(uid, path, request.data[RQ.DATA])
        return Response(rqStatus, status=status.HTTP_201_CREATED)

    elif request.method == RQ.GET:      # Get
        content = getObject(uid, path)

        if content is None:     # 가져온 파일이 없는경우
            return Response(status.HTTP_404_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        return HttpResponse(content, content_type=RQ.PDF, status=status.HTTP_200_OK)

    elif request.method == RQ.DELETE:       # Delete
        isDeleted = deleteObject(uid, path)

        if not isDeleted:   # 삭제가 되지 않은 경우
            return Response(status.HTTP_404_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        return Response(status.HTTP_200_OK, status=status.HTTP_200_OK)


@ api_view([RQ.GET])
def s3Contents(request, uid):
    listSerializer = ListSerializer(data={RQ.UID: uid})

    if not listSerializer.is_valid():
        return Response(status.HTTP_400_BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)

    if request.method == RQ.GET:        # Get
        contents = getList(uid)

        if contents is None:       # Content가 없으면
            return Response(status.HTTP_404_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        return JsonResponse({RQ.CONTENTS: contents}, status=status.HTTP_200_OK)
