from rest_framework import serializers
from classes.Elements import FileMeta

'''
    django REST framework에서 제공하는 serializer를 활용하여
    request로 받은 data를 역직렬화 하여 DB에 반영하고
    reponse로 사용 될 data를 다시 직렬화하여 json이나 xml등으로 손쉽게 변환이 가능하다.
'''


class FileSerializer(serializers.Serializer):       # file object
    uid = serializers.CharField(max_length=FileMeta.UID_LENGTH)
    dir = serializers.CharField(
        max_length=FileMeta.DIR_LENGTH, allow_blank=True)
    key = serializers.CharField(max_length=FileMeta.KEY_LENGTH)

    @property
    def elements(self):
        return self.data.values()


class ListSerializer(serializers.Serializer):       # list object
    uid = serializers.CharField(max_length=FileMeta.UID_LENGTH)
