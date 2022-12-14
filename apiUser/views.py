from django.http import JsonResponse, HttpResponse
from rest_framework.response import Response
from rest_framework import status, viewsets
from zipfile import ZipFile

from .s3 import *
from .serializers import FileSerializer, ListSerializer

from constants import REQUEST as RQ
from constants import RESPONSE as RP
from constants import FILEMETA, MESSAGE


class FileViewSet(viewsets.ModelViewSet):
    def retrieve(self, request):
        fileSerializer = FileSerializer(data=request.fileMeta)

        if fileSerializer.is_valid():
            uid, dir, key = fileSerializer.elements

            filePath = converter.dir2path(uid, dir, key)
            pdfContent, jsonContent = getObject(uid, filePath)

            if pdfContent is None or jsonContent is None:     # 가져온 파일이 없는경우
                return Response(MESSAGE.FILE_DOES_NOT_EXIST, status=status.HTTP_404_NOT_FOUND)

            # set response
            response = HttpResponse(
                content_type=RP.ZIP, status=status.HTTP_200_OK)
            response[RP.CONTENT_DISPOISTION] = RP.CONTENT_DISPOISTION_BODY

            # add zipFile and datas
            zipObj = ZipFile(response, 'w')
            zipObj.writestr(f"{key}.pdf", pdfContent)
            zipObj.writestr(f"{key}.json", jsonContent)

            return response

        else:
            return Response(MESSAGE.BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)

    def create(self, request):
        if request.data[RQ.DATA].size > FILEMETA.LIMITED_FILESIZE:
            return Response(MESSAGE.FILE_SIZE_EXCEEDED, status=status.HTTP_400_BAD_REQUEST)
        fileSerializer = FileSerializer(data=request.fileMeta)

        if fileSerializer.is_valid():
            uid, dir, key = fileSerializer.elements

            isCreated = createObject(uid, dir, key, request.data[RQ.DATA])

            if not isCreated:   # 생성이 되지 않은 경우
                return Response(MESSAGE.FILE_IS_NOT_CREATED, status=status.HTTP_404_NOT_FOUND)

            return Response(MESSAGE.FILE_IS_CREATED, status=status.HTTP_201_CREATED)
        else:
            error = fileSerializer.errors['key'][0].code
            if error == 'max_length':
                message = MESSAGE.MAX_LENGTH
            elif error == 'black':
                message = MESSAGE.BLANK
            else:
                message = MESSAGE.BAD_REQUEST

            return Response(message, status=status.HTTP_400_BAD_REQUEST)

    def destroy(self, request):
        fileSerializer = FileSerializer(data=request.fileMeta)
        if fileSerializer.is_valid():
            uid, dir, key = fileSerializer.elements

            filePath = converter.dir2path(uid, dir, key)
            isDeleted = deleteObject(uid, filePath)

            if not isDeleted:   # 삭제가 되지 않은 경우
                return Response(MESSAGE.FILE_IS_NOT_DELETED, status=status.HTTP_404_NOT_FOUND)

            return Response(MESSAGE.FILE_IS_DELETED, status=status.HTTP_200_OK)
        else:
            return Response(MESSAGE.BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)

    def update(self, request):
        fileSerializer = FileSerializer(data=request.fileMeta)

        if fileSerializer.is_valid():
            uid, dir, key = fileSerializer.elements

            filePath = converter.dir2path(uid, dir, key)
            isUpdated = saveJson(filePath, request.data[RQ.DATA])

            if not isUpdated:   # 생성이 되지 않은 경우
                return Response(MESSAGE.FILE_IS_NOT_SAVED, status=status.HTTP_404_NOT_FOUND)

            return Response(MESSAGE.FILE_IS_SAVED, status=status.HTTP_201_CREATED)
        else:
            return Response(MESSAGE.BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)


class ListViewSet(viewsets.ModelViewSet):
    def list(self, request):
        listSerializer = ListSerializer(data=request.fileMeta)

        if listSerializer.is_valid():
            uid = listSerializer.data[RQ.UID]
            contents = getList(uid)

            if contents is None:       # Content가 없으면
                return Response(MESSAGE.USER_INFO_IS_NOT_EXIST, status=status.HTTP_404_NOT_FOUND)

            return JsonResponse({RP.UID: uid, RP.CONTENTS: contents}, status=status.HTTP_200_OK)
        else:

            return Response(MESSAGE.BAD_REQUEST, status=status.HTTP_400_BAD_REQUEST)
