from django.urls import path
from . import views

'''
    파일 가져오기   GET	    https://<도메인>/file?key=(파일명)&dir=(디렉토리명)
    파일 삭제	    DELETE	https://<도메인>/file
    파일 올리기	    POST	https://<도메인>/file
    메타데이터 저장  PUT	 https://<도메인>/file
    
    파일 리스트	    GET	    https://<도메인>/list
'''

s3Object = views.FileViewSet.as_view({
    'get': 'retrieve',
    'post': 'create',
    'delete': 'destroy',
    'put': 'update'
})
s3Contents = views.ListViewSet.as_view({
    'get': 'list',
})

urlpatterns = [
    # User에 관한 API를 처리하는 view로 Request를 넘김
    path('file', s3Object),
    path('list', s3Contents),
]
