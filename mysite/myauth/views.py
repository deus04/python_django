from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.views import LogoutView
from django.contrib.auth.models import User
from django.http import HttpRequest, HttpResponse, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.urls import reverse, reverse_lazy
from django.views import View
from django.views.generic import TemplateView, CreateView, UpdateView, ListView, DetailView

from .forms import ProfileAvatarForm
from .models import Profile



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


class AboutMeView(LoginRequiredMixin, UpdateView):
    model = Profile
    form_class = ProfileAvatarForm
    template_name = 'myauth/about-me.html'

    def get_object(self, queryset=None):
        return self.request.user.profile

    def get_success_url(self):
        return reverse('myauth:about-me')


class UsersListView(ListView):
    model = User
    template_name = 'myauth/users-list.html'
    context_object_name = 'users'


class UserDetailView(DetailView):
    model = User
    template_name = 'myauth/user-detail.html'
    context_object_name = 'user_object'


class RegisterView(CreateView):
    form_class = UserCreationForm
    template_name = 'myauth/register.html'
    success_url = reverse_lazy('myauth:about-me')

    def form_valid(self, form):
        response = super().form_valid(form)
        Profile.objects.create(user=self.object)

        username = form.cleaned_data.get('username')
        password = form.cleaned_data.get('password1')
        user = authenticate(
            self.request,
            username=username,
            password=password,
        )
        login(request=self.request, user=user)
        return response


class ProfileUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = Profile
    form_class = ProfileAvatarForm
    template_name = 'myauth/profile-update.html'

    def test_func(self):
        profile = self.get_object()

        return (
            self.request.user.is_staff
            or profile.user == self.request.user
        )

    def get_success_url(self):
        return reverse(
            'myauth:user-detail',
            kwargs={'pk': self.object.user.pk}
        )


def logout_view(request: HttpRequest):
    logout(request)
    return redirect(reverse('myauth:login'))


class MyLogoutView(View):
    def get(self, request):
        logout(request)
        return redirect('myauth:login')


#@user_passes_test(lambda u: u.is_superuser)
def set_cookie_view(request:HttpRequest) -> HttpResponse:
    response = HttpResponse('Cookie set')
    response.set_cookie('fizz', 'buzz', max_age=3600)
    return response


def get_cookie_view(request:HttpRequest) -> HttpResponse:
    value = request.COOKIES.get('fizz', 'default value')
    return HttpResponse(f'Cookie value: {value!r}')


@permission_required('myauth.view_profile', raise_exception=True)
def set_session_view(request:HttpRequest) -> HttpResponse:
    response = HttpResponse('Session set!')
    request.session['foobar'] = 'spameggs'
    return response


@login_required
def get_session_view(request:HttpRequest) -> HttpResponse:
    value = request.session.get('foobar', 'default')
    response = HttpResponse(f'Session value: {value!r}')
    return response


class FooBarView(View):
    def get(self, request:HttpRequest) -> JsonResponse:
        return JsonResponse({"foo": "bar", "spam": "eggs"})
