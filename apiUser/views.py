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

    if fileSerializer.is_valid():
        path = f"{uid}/{keyName}"
        if request.method == RQ.POST:
            rqStatus = createObject(uid, path, request.data[RQ.DATA])
            return Response(rqStatus, status=status.HTTP_201_CREATED)

        elif request.method == RQ.GET:
            content = getObject(uid, path)
            if content is not None:
                return HttpResponse(
                    content, content_type=RQ.PDF, status=status.HTTP_200_OK)
            else:
                return Response(status.HTTP_404_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

        elif request.method == RQ.DELETE:
            isDeleted = deleteObject(uid, path)

            # 정상 삭제된 경우
            if isDeleted:
                return Response(status.HTTP_200_OK, status=status.HTTP_200_OK)
            else:
                return Response(status.HTTP_404_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)

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
                return Response(status.HTTP_404_NOT_FOUND, status=status.HTTP_404_NOT_FOUND)
    else:
        return Response(listSerializer.errors, status=status.HTTP_400_BAD_REQUEST)
