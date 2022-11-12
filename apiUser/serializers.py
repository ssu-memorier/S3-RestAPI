from rest_framework import serializers
from .models import Content

'''
    django REST framework에서 제공하는 serializer를 활용하여
    request로 받은 data를 역직렬화 하여 DB에 반영하고
    reponse로 사용 될 data를 다시 직렬화하여 json이나 xml등으로 손쉽게 변환이 가능하다.
'''


class FileSerializer(serializers.ModelSerializer):       # file object
    class Meta:
        model = Content
        fields = '__all__'

    def create(self, validated_data):
        return Content.objects.create(**validated_data)


class ListSerializer(serializers.Serializer):       # list object
    uid = serializers.CharField(max_length=128)
