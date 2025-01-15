from django.contrib import admin
from django.urls import path
from .views import process_get_view, user_form, handle_file_upload, exception_file_upload


app_name = 'requestdataapp'
urlpatterns = [
    path('get/', process_get_view, name='get-view'),
    path('bio/', user_form, name='user_form'),
    path('upload/', handle_file_upload, name='file_upload'),
    path('upload-exception/', exception_file_upload, name='exception-file-upload'),

]
