from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view

from .s3 import *
from .serializers import FileSerializer, ListSerializer

from constants import REQUEST as RQ


@api_view([RQ.GET, RQ.POST, RQ.DELETE])
def s3Object(request, uid, keyName):
    print(uid, keyName)
    fileSerializer = FileSerializer(data={RQ.UID: uid, RQ.KEYNAME: keyName})

    if fileSerializer.is_valid():
        path = f"{uid}/{keyName}"
        if request.method == RQ.POST:
            putObject(path, request.data[RQ.DATA])
            return Response(RQ.SUCCESS, status=status.HTTP_200_OK)

        elif request.method == RQ.GET:
            content = getObject(uid, path)
            if content is not None:
                return HttpResponse(
                    content, content_type=RQ.PDF, status=status.HTTP_200_OK)
            else:
                return Response(RQ.FAIL, status=status.HTTP_400_BAD_REQUEST)

        elif request.method == RQ.DELETE:
            isDeleted = deleteObject(uid, path)

            # 정상 삭제된 경우
            if isDeleted:
                return Response(RQ.SUCCESS, status=status.HTTP_200_OK)
            else:
                return Response(RQ.FAIL, status=status.HTTP_400_BAD_REQUEST)

    else:
        return Response(fileSerializer.errors, status=status.HTTP_400_BAD_REQUEST)


@ api_view([RQ.GET])
def s3Contents(request, uid):
    listSerializer = ListSerializer(data={RQ.UID: uid})
    if listSerializer.is_valid():
        if request.method == RQ.GET:
            contents = getList(uid)
            if contents is not None:
                return JsonResponse({RQ.CONTENTS: contents}, status=status.HTTP_200_OK)
            else:
                return Response(None, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response(listSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
