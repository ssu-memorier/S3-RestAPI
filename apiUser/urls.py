from django.urls import path
from . import views

'''
    파일 가져오기   GET	    https://<도메인>/file/userA/folderA/.../*
    파일 삭제	    DELETE	https://<도메인>/file/userA/folderA/.../*
    파일 올리기	    POST	https://<도메인>/file/userA/folderA/.../*
    
    파일 리스트	    GET	    https://<도메인>/list/userA
    메타데이터 저장  PUT	 https://<도메인>/save/userA/folderA/.../*
'''

s3Object = views.FileViewSet.as_view({
    'get': 'retrieve',
    'post': 'create',
    'delete': 'destroy',
})
s3Contents = views.ListViewSet.as_view({
    'get': 'list',
})

s3MetaSave = views.MetaViewSet.as_view({
    'put': 'update'
})

urlpatterns = [
    # User에 관한 API를 처리하는 view로 Request를 넘김
    path('file/<str:uid>/<path:keyName>', s3Object),
    path('list/<str:uid>', s3Contents),
    path('save/<str:uid>/<path:keyName>', s3MetaSave),
]
