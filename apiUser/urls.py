from django.urls import path
from . import views

'''
    파일 가져오기   GET	    https://gomguk.net/s3contents/file/userA/folderA/.../*.pdf
    파일 삭제	    DELETE	https://gomguk.net/s3contents/file/userA/folderA/.../*.pdf
    파일 올리기	    POST	https://gomguk.net/s3contents/file/userA/folderA/.../*.pdf
    
    파일 리스트	    GET	    https://gomguk.net/s3contents/list/userA
'''

urlpatterns = [
    # User에 관한 API를 처리하는 view로 Request를 넘김
    path('file/<str:uid>/<path:keyName>', views.s3Object),
    path('list/<str:uid>', views.s3Contents),
]
