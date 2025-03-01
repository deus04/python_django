from django.contrib.auth.views import LogoutView
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views import View


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            return redirect('/admin/')

        return render(request, 'myauth/login.html')

    username = request.POST['username']
    password = request.POST['password']

    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        return redirect('/admin/')

    return render(request, 'myauth/login.html', {'error': 'Invalid login credentials'})


def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse('myauth:login'))


#class MyLogoutView(LogoutView):
   # next_page = reverse_lazy('myauth:login')


class MyLogoutPage(View):
    def get(self, request):
        logout(request)
        return redirect('myauth:login')




def set_cookie_view(request:HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response


def get_cookie_view(request:HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f'Cookie value: {value!r}')


def set_session_view(request:HttpRequest) -> HttpResponse:
    response = HttpResponse('Session set!')
    request.session['foobar'] = 'spameggs'
    return response


def get_session_view(request:HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default')
    response = HttpResponse(f'Session value: {value!r}')
    return response
























