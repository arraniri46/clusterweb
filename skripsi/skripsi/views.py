from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from kmodes.kprototypes import KPrototypes
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django import forms
import pandas as pd
import pickle as pk
import numpy as np
import os
import _pickle as cPickle
import json


#BACA FILE UPLOADED
file_ = os.path.join(settings.BASE_DIR, 'media/data2pkl.pkl')
# file_pickle = 

def index(request):
    context = {
        'title' : 'Index'
    }
    return render(request, 'index.html', context)

def home(request):
    return render(request, 'home.html')

def result(request):
    return render(request, 'result.html')

def charts(request):
    return render(request, 'base/charts.html')

def maps(request):
    return render(request, 'base/map.html')

def dataVendor(request):

    df = pd.read_pickle(file_)
    
    total_kendaraan = df['MERK'].value_counts().sum().tolist()
    vendor_kendaraan = df['MERK'].value_counts(sort=False).rename_axis('MERK').reset_index(name='total_merk')
    list_vendor_kendaraan = vendor_kendaraan['MERK'].str.strip().tolist()
    data_vendor_kendaraan = vendor_kendaraan['total_merk'].tolist()

    context = {
        'total' : total_kendaraan,
        'label_vendor' : list_vendor_kendaraan,
        'data_vendor' : data_vendor_kendaraan,
    }

    return render(request, 'data_vendor.html', context)

def dataPekerjaan(request):

    df = pd.read_pickle(file_)
    
    pekerjaan = df[['PEKERJAAN']][~df['PEKERJAAN'].isin(['-'])]
    total_pekerjaan = pekerjaan['PEKERJAAN'].value_counts().sum().tolist()
    new_pekerjaan = pekerjaan['PEKERJAAN'].value_counts(sort=False).rename_axis('PEKERJAAN').reset_index(name='total_pekerjaan')
    list_pekerjaan = new_pekerjaan['PEKERJAAN'].str.strip().tolist()
    data_pekerjaan = new_pekerjaan['total_pekerjaan'].tolist()

    context = {
        'total' : total_pekerjaan,
        'label_pekerjaan' : list_pekerjaan,
        'data_pekerjaan' : data_pekerjaan,
    }

    return render(request, 'data_pekerjaan.html', context)

def dashboard(request):
    df = pd.read_pickle(file_)
    # df = df[['KABUPATEN', 'PEKERJAAN', 'OBJECT', 'TENOR', 'OTR','cluster']]
    # df2 = df[['PEKERJAAN', 'OBJECT', 'TENOR', 'OTR','cluster']]

    df = df[['KABUPATEN', 'PEKERJAAN', 'OBJECT', 'TENOR', 'OTR']]
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

    # # CLUSTERING
    # kp = KPrototypes(n_clusters=4, init='Huang')
    # cluster = kp.fit_predict(df2, categorical=[0,1,2])
    # df['cluster'] = cluster

    # PARSING DATA CLUSTER
    # dataCluster = df['cluster'].astype(str)
    # dataCluster = dataCluster.value_counts(sort=False).rename_axis('cluster').reset_index(name='totalCluster')
    # listCluster = dataCluster['cluster'].str.strip().tolist()
    # listDataCluster = dataCluster['totalCluster'].tolist()

    # # PARSING DATA CLUSTER MAP
    # df_cluster_0 = df2.loc[df2['cluster'] == 0]
    # df_cluster_0 = df_cluster_0['cluster'].value_counts().tolist()

    # df_cluster_1 = df2.loc[df2['cluster'] == 1]
    # df_cluster_1 = df_cluster_1['cluster'].value_counts()

    # df_cluster_2 = df2.loc[df2['cluster'] == 2]
    # df_cluster_2 = df_cluster_2['cluster'].value_counts()

    # KATEGORI PROPERTIES MAP
    columnKategori = []
    for kol in df.columns:
        columnKategori.append(kol)

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
        'kolomKategori' : columnKategori,
        # 'df_cluster_0' : df_cluster_0,
        # 'df_cluster_1' : df_cluster_1,
        # 'df_cluster_2' : df_cluster_2,
    }
    return render(request, 'dashboard.html', context)

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
    

#SHOW FILE KE DATATABLE HTML
def table(request):

    # df = pd.read_csv(file_)
    
    # pickleIn = open(file_,'rb')
    # df = cPickle.load(pickleIn)

    # df = df[['ID','KABUPATEN', 'PEKERJAAN', 'OBJECT', 'TENOR', 'STATUS']]
    # allData = []

    # for i in range(df.shape[0]):
    #     temp = df.iloc[i]
    #     allData.append(dict(temp))
    # context = {
    #     'data' : allData
    # }

    return render(request, 'base/table.html')

def dataJson(request):

    df = pd.read_pickle(file_)
    df2 = df[['ID','KABUPATEN', 'PEKERJAAN', 'OBJECT', 'TENOR' ,'OTR']].astype(str)
    df3 = df2.apply(lambda x: x.str.strip() if x.dtype == "object" else x)
    allData = []

    for i in range(df3.shape[0]):
        temp = df3.iloc[i]
        allData.append(dict(temp))
        #dataJson = json.dumps(allData)

    context = {
        "data" : allData
    }

    return JsonResponse(context)
