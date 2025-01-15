from django.core.files.storage import FileSystemStorage
from django.http import HttpRequest, HttpResponse
from django.shortcuts import render

# Create your views here.

def process_get_view(request: HttpRequest) -> HttpResponse:
    a = request.GET.get('a','')
    b = request.GET.get('b','')
    result = a + b
    context = {
        'a':a,
        'b':b,
        'result': result,
    }
    return render(request, "requestdataapp/request-query-params.html", context=context)


def user_form(request: HttpRequest) -> HttpResponse:
    return render(request, 'requestdataapp/user-bio-form.html')

def handle_file_upload(request: HttpRequest) -> HttpResponse:
    if request.method == 'POST' and request.FILES.get('myfile'):
        myfile = request.FILES['myfile']
        if myfile.size > 2097152:
            return exception_file_upload(request)

        fs = FileSystemStorage()
        filename = fs.save(myfile.name,myfile)
        print('saved file', filename)

    return render(request, 'requestdataapp/file-upload.html')

def exception_file_upload(request):
    return render(request, 'requestdataapp/exception-file-upload.html')