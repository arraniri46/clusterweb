from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from kmodes.kprototypes import KPrototypes
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django import forms
import pandas as pd
import numpy as np
import os

def index(request):
    context = {
        'title' : 'Index'
    }
    return render(request, 'index.html', context)

def dashboard(request):
    return render(request, 'dashboard.html')

def home(request):
    return render(request, 'home.html')

def charts(request):
    return render(request, 'base/charts.html')

def map(request):
    return render(request, 'base/map.html')

def table(request):
    return render(request, 'base/table.html')

def result(request):
    return render(request, 'result.html')

class UploadFileForm(forms.Form):
    file = forms.FileField()

def upload(request):
    context = {}
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form = request.FILES['file']
            fs = FileSystemStorage()
            name = fs.save(form.name, form)
            context['url'] = fs.url(name)

            return HttpResponseRedirect('/home/')

    else:
        form = UploadFileForm()

    return render(request, 'upload.html', context)
    

    # def data_view(request):
    #     filename = 'media/'+ filename

    #     df = pd.read_excel(filename)

    #     return render(request, 'example.html', {'DataFrame' : df})

    # df = pd.read_csv(os.path.join(path, str(request.FILES['file'])))
    # table_content = df.to_html()
    # context = {'table_content': table_content}
    # return render(request, 'index.html', context)

file_ = os.path.join(settings.BASE_DIR, 'media/download.csv')

def example(request):

    df = pd.read_csv(file_)
    table = df.to_html(classes=['table','table-hover'])

    context = {'table': table}
    return render(request, 'example.html', context)