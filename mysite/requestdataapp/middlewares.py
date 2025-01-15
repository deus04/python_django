import datetime
from time import time
from fileinput import close

from django.http import HttpRequest
from django.shortcuts import render



def set_useragent_on_request_middleware(get_response):
    print('initial call')
    def middleware(request: HttpRequest):
        print('before get response')
        request.user_agent = request.META['HTTP_USER_AGENT']
        response = get_response(request)
        print('after get response')
        return response
    return middleware


class CountRequestsMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.requests_count = 0
        self.responses_count = 0
        self.exceptions_count = 0
        self.users_id_dict = dict()

    def __call__(self, request: HttpRequest):
        self.requests_count += 1
        print('requests count', self.requests_count)
        if self.throttling_middleware(request):
            response = render(request, 'requestdataapp/exception-throttling_middleware.html')
        else:
            response = self.get_response(request)
        self.responses_count += 1
        print('responses count', self.responses_count)
        return response

    def process_exception(self, request: HttpRequest, exception: Exception):
        self.exceptions_count += 1
        print('got', self.exceptions_count, 'exceptions so far')


    def throttling_middleware(self, request):
        user_id = request.META['REMOTE_ADDR']
        if user_id in self.users_id_dict:
            if time() - self.users_id_dict[user_id] < 5:
                self.users_id_dict[user_id] = time()
                return True
            else:
                self.users_id_dict[user_id] = time()
                return False
        else:
            self.users_id_dict[user_id] = time()
            return False

