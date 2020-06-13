from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from kmodes.kprototypes import KPrototypes
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django import forms
import pandas as pd
import numpy as np
import os
import json

#BACA FILE UPLOADED
file_ = os.path.join(settings.BASE_DIR, 'media/EXCELnasabahTraining.xlsx')

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
    df = pd.read_excel(file_)
    df = df[['ID','KABUPATEN', 'PEKERJAAN', 'OBJECT', 'TENOR', 'STATUS', 'OTR']]
    df2 = df[['PEKERJAAN', 'OBJECT', 'TENOR', 'OTR']]
    pekerjaan = df['PEKERJAAN']
    objectKendaraan = df['OBJECT']
    tenor = df['TENOR'].astype(str)

    #dataAkhir = pd.DataFrame(df['cluster'].value_counts())
    #labelPekerjaan = pd.DataFrame(data = df[['PEKERJAAN']].groupby(['PEKERJAAN']).sum().sort_values(by='PEKERJAAN', ascending=False)).reset_index()
    #totalPekerjaan = pd.DataFrame(data = df['PEKERJAAN'].value_counts(sort=False).tolist(), columns=['total'])

    #PARSING DATA PEKERJAAN
    pekerjaan = pekerjaan.value_counts(sort=False).rename_axis('PEKERJAAN').reset_index(name='totalPekerjaan')
    listPekerjaan = pekerjaan['PEKERJAAN'].str.strip().tolist()
    listDataPekerjaan = pekerjaan['totalPekerjaan'].tolist()

    #PARSING DATA KENDARAAN
    objectKendaraan = objectKendaraan.value_counts(sort=False).rename_axis('OBJECT').reset_index(name='totalKendaraan')
    listKendaraan = objectKendaraan['OBJECT'].str.strip().tolist()
    listDataKendaraan = objectKendaraan['totalKendaraan'].tolist()

    #PARSING DATA TENOR
    tenor = tenor.value_counts(sort=False).rename_axis('TENOR').reset_index(name='totalTenor')
    listTenor = tenor['TENOR'].str.strip().tolist()
    listDataTenor = tenor['totalTenor'].tolist()

    #CLUSTERING
    # kp = KPrototypes(n_clusters=4, init='Huang')
    # cluster = kp.fit_predict(df2, categorical=[0,1,2])
    # df['cluster'] = cluster

    #PARSING DATA CLUSTER
    # dataCluster = df['cluster'].astype(str)
    # dataCluster = dataCluster.value_counts(sort=False).rename_axis('cluster').reset_index(name='totalCluster')
    # listCluster = dataCluster['cluster'].str.strip().tolist()
    # listDataCluster = dataCluster['totalCluster'].tolist()

    allData = []

    for i in range(df.shape[0]):
        temp = df.iloc[i]
        allData.append(dict(temp))

    context = {
        'data' : allData,
        'pekerjaan' : pekerjaan,
        'labelPekerjaan' : listPekerjaan,
        'dataPekerjaan' : listDataPekerjaan,
        'labelKendaraan' : listKendaraan,
        'dataKendaraan' : listDataKendaraan,
        'labelTenor' : listTenor,
        'dataTenor' : listDataTenor,
        # 'labelCluster' : listCluster,
        # 'dataCluster' : listDataCluster,
    }
    return render(request, 'result.html', context)

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

#SHOW FILE KE DATATABLE HTML
def example(request):

    df = pd.read_excel(file_)
    df = df[['ID','KABUPATEN', 'PEKERJAAN', 'OBJECT', 'TENOR', 'STATUS']]
    allData = []

    for i in range(df.shape[0]):
        temp = df.iloc[i]
        allData.append(dict(temp))
    context = {
        'data' : allData
    }

    return render(request, 'base/example.html', context)

def dataJson(request):

    df = pd.read_excel(file_, dtype=str)
    df = df[['ID','KABUPATEN', 'PEKERJAAN', 'OBJECT', 'TENOR', 'STATUS']]
    allData = []

    for i in range(df.shape[0]):
        temp = df.iloc[i]
        allData.append(dict(temp))
        dataJson = json.dumps(allData)

    context = {
        "data" : dataJson
    }

    return JsonResponse(context)