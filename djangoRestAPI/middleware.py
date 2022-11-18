from utils import elements, converter
from constants import REQUEST as RQ
from django.http import HttpResponseForbidden
from rest_framework import status
import json
"""
    Rest Framework 을 위한 전용 커스텀 미들웨어에 대해 response format 을 자동으로 세팅
"""


class LogInMiddleware:
    METHOD = ('GET', 'POST', 'PUT', 'DELETE')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        print('a ///', '\t', request.headers)
        print('b ///', '\t', request.__dict__)
        print('c ///', '\t', request.COOKIES)
        # loaded = json.loads(request.COOKIES[RQ.COOKIES_TOKEN])
        # jwtToken = loaded[RQ.TOKEN]

        jwtToken = request.COOKIES[RQ.COOKIES_TOKEN]
        decoded = converter.jwtTokenDecoder(jwtToken)
        if decoded is None:  # 잘못된 JWT 토큰이 들어올시 권한이 없다는 오류코드를 반환합니다.
            return HttpResponseForbidden(status.HTTP_401_UNAUTHORIZED)
        if not hasattr(request, 'uid'):
            request.uid = elements.getUid(
                decoded['email'], decoded['provider'])
        response = self.get_response(request)

        return response


class SerializerMiddleware:
    METHOD = ('GET', 'POST', 'PUT', 'DELETE')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        uid = request.uid

        if request.path == '/list':
            myRequest = {'uid': uid}

        else:
            if request.method == 'GET':
                myRequest = request.GET.copy()
                myRequest['uid'] = uid

            elif request.method == "POST":
                print(">>>>>>", request.POST)
                myRequest = request.POST.copy()
                myRequest['uid'] = uid

            elif request.method == 'DELETE' or request.method == 'PUT':
                myRequest = json.loads(request.body)
                myRequest['uid'] = uid

            if not hasattr(request, 'fileMeta'):
                request.fileMeta = myRequest
            response = self.get_response(request)

        return response
