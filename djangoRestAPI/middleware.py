from utils import elements, converter
from constants import REQUEST as RQ
from django.http import HttpResponseForbidden
from rest_framework import status

import json
import os
import requests
from dotenv import load_dotenv
from urllib.parse import urljoin

from constants import KEY
"""
    Rest Framework 을 위한 전용 커스텀 미들웨어에 대해 response format 을 자동으로 세팅
"""


load_dotenv()   # load .env
authUrl = os.environ.get(KEY.AUTH_URL)


class LogInMiddleware:
    METHOD = ('GET', 'POST', 'PUT', 'DELETE')

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        jwtToken = request.COOKIES[RQ.COOKIES_TOKEN]

        # Request에서 쿠키를 받아 다시 재가공한 뒤 AUTH 서버에 유효성 검사를 진행
        params = {'jwt': jwtToken}
        url = urljoin(authUrl, RQ.AUTH_VALIDTOKEN_URL)
        response = requests.get(url, params=params)  # 요청 전송

        # 잘못된 요청 진행
        if response.status_code == 401:
            return HttpResponseForbidden(status.HTTP_401_UNAUTHORIZED)

        # Decode 진행
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
                myRequest = request.POST.copy()
                myRequest['uid'] = uid

            elif request.method == 'DELETE' or request.method == 'PUT':
                myRequest = json.loads(request.body)
                myRequest['uid'] = uid

        if not hasattr(request, 'fileMeta'):
            request.fileMeta = myRequest
        response = self.get_response(request)

        return response
