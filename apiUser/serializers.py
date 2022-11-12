from rest_framework import serializers

'''
    django REST framework에서 제공하는 serializer를 활용하여
    request로 받은 data를 역직렬화 하여 DB에 반영하고
    reponse로 사용 될 data를 다시 직렬화하여 json이나 xml등으로 손쉽게 변환이 가능하다.
'''


class FileSerializer(serializers.Serializer):       # file object
    uid = serializers.CharField(max_length=64)
    dir = serializers.CharField(max_length=200, allow_blank=True)
    key = serializers.CharField(max_length=100)


class ListSerializer(serializers.Serializer):       # list object
    uid = serializers.CharField(max_length=64)
