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
import random
import xlrd
import matplotlib.pyplot as plt 

from .forms import FormField, UploadFileForm


#BACA FILE UPLOADED
file_ = os.path.join(settings.BASE_DIR, 'media/data.xlsx')
# file_pickle = 

def index(request):
    context = {
        'title' : 'Index'
    }
    return render(request, 'index.html', context)

def result(request):
    return render(request, 'result.html')   

def charts(request):
    return render(request, 'base/charts.html')

def maps(request):
    return render(request, 'base/map.html')

def dataKendaraan(request):

    files_ = os.path.join(settings.BASE_DIR, 'media\\'+request.session.get('file'))
    df = pd.read_excel(files_)
    
    total_kendaraan = df['OBJECT'].value_counts().sum().tolist()
    jenis_kendaraan = df['OBJECT'].value_counts(sort=False).rename_axis('OBJECT').reset_index(name='total_object_kendaraan')
    list_jenis_kendaraan = jenis_kendaraan['OBJECT'].str.strip().tolist()
    data_jenis_kendaraan = jenis_kendaraan['total_object_kendaraan'].tolist()

    context = {
        'total' : total_kendaraan,
        'label_jenis_kendaraan' : list_jenis_kendaraan,
        'data_jenis_kendaraan' : data_jenis_kendaraan,
    }

    return render(request, 'data_kendaraan.html', context)

def dataVendor(request):

    files_ = os.path.join(settings.BASE_DIR, 'media\\'+request.session.get('file'))
    df = pd.read_excel(files_)
    
    total_vendor_kendaraan = df['MERK'].value_counts().sum().tolist()
    vendor_kendaraan = df['MERK'].value_counts(sort=False).rename_axis('MERK').reset_index(name='total_merk')
    list_vendor_kendaraan = vendor_kendaraan['MERK'].str.strip().tolist()
    data_vendor_kendaraan = vendor_kendaraan['total_merk'].tolist()

    zipped_vendor = zip(list_vendor_kendaraan, data_vendor_kendaraan)

    context = {
        'total' : total_vendor_kendaraan,
        'label_vendor' : list_vendor_kendaraan,
        'data_vendor' : data_vendor_kendaraan,
        'zipped_vendor' : zipped_vendor,
    }

    return render(request, 'data_vendor.html', context)

def dataPekerjaan(request):

    files_ = os.path.join(settings.BASE_DIR, 'media\\'+request.session.get('file'))
    df = pd.read_excel(files_)
    
    pekerjaan = df[['PEKERJAAN']][~df['PEKERJAAN'].isin(['-'])]
    total_pekerjaan = pekerjaan['PEKERJAAN'].value_counts().sum().tolist()
    new_pekerjaan = pekerjaan['PEKERJAAN'].value_counts(sort=False).rename_axis('PEKERJAAN').reset_index(name='total_pekerjaan')
    list_pekerjaan = new_pekerjaan['PEKERJAAN'].str.strip().tolist()
    data_pekerjaan = new_pekerjaan['total_pekerjaan'].tolist()

    zipped_pekerjaan = zip(list_pekerjaan, data_pekerjaan)

    context = {
        'total' : total_pekerjaan,
        'label_pekerjaan' : list_pekerjaan,
        'data_pekerjaan' : data_pekerjaan,
        'zipped_pekerjaan' : zipped_pekerjaan,
    }

    return render(request, 'data_pekerjaan.html', context)

def dashboard(request):
    files_ = os.path.join(settings.BASE_DIR, 'media\\'+request.session.get('file'))
    df = pd.read_excel(files_)
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
    pekerjaan = pekerjaan.value_counts().rename_axis('PEKERJAAN').reset_index(name='totalPekerjaan')
    listPekerjaan = pekerjaan['PEKERJAAN'].str.strip().tolist()
    # listPekerjaan.sort()
    listDataPekerjaan = pekerjaan['totalPekerjaan'].tolist()
    # listDataPekerjaan.sort()

    #PARSING DATA KENDARAAN
    objectKendaraan = objectKendaraan.value_counts().rename_axis('OBJECT').reset_index(name='totalKendaraan')
    listKendaraan = objectKendaraan['OBJECT'].str.strip().tolist()
    # listKendaraan.sort()
    listDataKendaraan = objectKendaraan['totalKendaraan'].tolist()
    # listDataKendaraan.sort()

    #PARSING DATA TENOR
    tenor = tenor.value_counts().rename_axis('TENOR').reset_index(name='totalTenor')
    listTenor = tenor['TENOR'].str.strip().tolist()
    # listTenor.sort()
    listDataTenor = tenor['totalTenor'].tolist()
    # listDataTenor.sort()

    # CLUSTERING
    input_cluster = int(request.session.get('jumlah_cluster'))

    kp = KPrototypes(n_clusters=input_cluster, init='Huang', verbose=2, n_jobs=-1, max_iter=10, random_state=42)
    cluster = kp.fit_predict(df, categorical=[0,1,2,3])
    df['cluster'] = cluster+1

    # request.session['dataframe'] = cluster
    global datafarame
    def datafarame():
        return cluster

    # PARSING DATA CLUSTER
    dataCluster = df['cluster'].astype(str)
    dataCluster = dataCluster.value_counts().rename_axis('cluster').reset_index(name='totalCluster')
    listCluster = dataCluster['cluster'].str.strip().tolist()
    # listCluster.sort()
    listDataCluster = dataCluster['totalCluster'].tolist()
    # listDataCluster.sort()

    # PARSING DATA CLUSTER MAP
    df_cluster_0 = df.loc[df['cluster'] == 0]
    df_cluster_0 = df_cluster_0['cluster'].value_counts().tolist()

    df_cluster_1 = df.loc[df['cluster'] == 1]
    df_cluster_1 = df_cluster_1['cluster'].value_counts()

    df_cluster_2 = df.loc[df['cluster'] == 2]
    df_cluster_2 = df_cluster_2['cluster'].value_counts()

    # KATEGORI PROPERTIES MAP
    columnKategori = []
    for kol in df.columns:
        columnKategori.append(kol)

    allData = []
    for i in range(df.shape[0]):
        temp = df.iloc[i]
        allData.append(dict(temp))

    # topCluster    
    data1 = df['KABUPATEN'].where(df['cluster'] == 1).value_counts().to_dict()
    data2 = df['KABUPATEN'].where(df['cluster'] == 2).value_counts().to_dict()
    data3 = df['KABUPATEN'].where(df['cluster'] == 3).value_counts().to_dict()
    
    columnList = list(df.columns)
    del columnList[-1]

    dictWilayah_1 = df['KABUPATEN'].where(df['cluster'] == 1).str.strip().value_counts().iloc[0:3].to_dict()
    dictPekerjaan_1 = df['PEKERJAAN'].where(df['cluster'] == 1).str.strip().value_counts().iloc[0:3].to_dict()
    dictObjek_1 = df['OBJECT'].where(df['cluster'] == 1).str.strip().value_counts().iloc[0:3].to_dict()
    dictTenor_1 = df['TENOR'].astype(str).where(df['cluster'] == 1).str.strip().value_counts().iloc[0:3].to_dict()

    # dictWilayah_2 = df['KABUPATEN'].where(df['cluster'] == 2).str.strip().value_counts().iloc[0:3].to_dict()
    # dictPekerjaan_2 = df['PEKERJAAN'].where(df['cluster'] == 2).str.strip().value_counts().iloc[0:3].to_dict()
    # dictObjek_2 = df['OBJECT'].where(df['cluster'] == 2).str.strip().value_counts().iloc[0:3].to_dict()
    # dictTenor_2 = df['TENOR'].astype(str).where(df['cluster'] == 2).str.strip().value_counts().iloc[0:3].to_dict()

    # dictWilayah_3 = df['KABUPATEN'].where(df['cluster'] == 3).str.strip().value_counts().iloc[0:3].to_dict()
    # dictPekerjaan_3 = df['PEKERJAAN'].where(df['cluster'] == 3).str.strip().value_counts().iloc[0:3].to_dict()
    # dictObjek_3 = df['OBJECT'].where(df['cluster'] == 3).str.strip().value_counts().iloc[0:3].to_dict()
    # dictTenor_3 = df['TENOR'].astype(str).where(df['cluster'] == 3).str.strip().value_counts().iloc[0:3].to_dict()

    if request.method == 'POST':
        if request.POST.get('1'):
            dictWilayah_1 = df['KABUPATEN'].where(df['cluster'] == 1).str.strip().value_counts().iloc[0:3].to_dict()
            dictPekerjaan_1 = df['PEKERJAAN'].where(df['cluster'] == 1).str.strip().value_counts().iloc[0:3].to_dict()
            dictObjek_1 = df['OBJECT'].where(df['cluster'] == 1).str.strip().value_counts().iloc[0:3].to_dict()
            dictTenor_1 = df['TENOR'].astype(str).where(df['cluster'] == 1).str.strip().value_counts().iloc[0:3].to_dict()

        elif request.POST.get('2'):
            dictWilayah_1 = df['KABUPATEN'].where(df['cluster'] == 2).str.strip().value_counts().iloc[0:3].to_dict()
            dictPekerjaan_1 = df['PEKERJAAN'].where(df['cluster'] == 2).str.strip().value_counts().iloc[0:3].to_dict()
            dictObjek_1 = df['OBJECT'].where(df['cluster'] == 2).str.strip().value_counts().iloc[0:3].to_dict()
            dictTenor_1 = df['TENOR'].astype(str).where(df['cluster'] == 2).str.strip().value_counts().iloc[0:3].to_dict()

        elif request.POST.get('3'):
            dictWilayah_1 = df['KABUPATEN'].where(df['cluster'] == 3).str.strip().value_counts().iloc[0:3].to_dict()
            dictPekerjaan_1 = df['PEKERJAAN'].where(df['cluster'] == 3).str.strip().value_counts().iloc[0:3].to_dict()
            dictObjek_1 = df['OBJECT'].where(df['cluster'] == 3).str.strip().value_counts().iloc[0:3].to_dict()
            dictTenor_1 = df['TENOR'].astype(str).where(df['cluster'] == 3).str.strip().value_counts().iloc[0:3].to_dict()



    # for i in range(1,max(cluster+2)):
    


    context = {
        'data' : allData,
        'pekerjaan' : pekerjaan,
        'labelPekerjaan' : listPekerjaan,
        'dataPekerjaan' : listDataPekerjaan,
        'labelKendaraan' : listKendaraan,
        'dataKendaraan' : listDataKendaraan,
        'labelTenor' : listTenor,
        'dataTenor' : listDataTenor,
        'labelCluster' : listCluster,
        'dataCluster' : listDataCluster,
        'kolomKategori' : columnKategori,
        'df_cluster_0' : df_cluster_0,
        'df_cluster_1' : df_cluster_1,
        'df_cluster_2' : df_cluster_2,
        'clusters' : cluster,
        'data3' : data3,
        'data2' : data2,
        'data1' : data1,
        'columnName' : columnList,
        'dictWilayah' : dictWilayah_1,
        'dictPekerjaan' : dictPekerjaan_1,
        'dictObjek' : dictObjek_1,
        'dictTenor' : dictTenor_1,
        # 'dictWilayah' : dictWilayah_2,
        # 'dictPekerjaan' : dictPekerjaan_2,
        # 'dictObjek' : dictObjek_2,
        # 'dictTenor' : dictTenor_2,
        # 'dictWilayah' : dictWilayah_3,
        # 'dictPekerjaan' : dictPekerjaan_3,
        # 'dictObjek' : dictObjek_3,
        # 'dictTenor' : dictTenor_3,
       
    }
    return render(request, 'dashboard.html', context)

#FUNGSI UPLOAD MASIH BERMASALAHH
def upload(request):
    
    form_field = FormField()
    context = {
        'title' : str('Home - Upload File'),
        'form_field' : form_field
    }
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form = request.FILES['file']
            request.session['file'] = request.FILES['file'].name
            
            # request.session['file'] = form
            fs = FileSystemStorage()
            fs.save(form.name, form)
            # context['url'] = fs.url(name)
        
        input_n_cluster = FormField(request.POST)
        if input_n_cluster.is_valid():
            request.session['jumlah_cluster'] = request.POST['jumlah_cluster']

            return HttpResponseRedirect('/dashboard/')

    else:
        form = UploadFileForm()

    return render(request, 'upload.html', context)

def elbowGraph(request):

    form_field = FormField()
    context = {
        'form_field' : form_field
    }
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            form = request.FILES['file']
            # request['file'] = request.FILES['file'].name
            
            # request.session['file'] = form
            fs = FileSystemStorage()
            fs.save(form.name, form)
            # context['url'] = fs.url(name)
            df = pd.read_excel(form)
            df = df[['KABUPATEN', 'PEKERJAAN', 'OBJECT', 'TENOR', 'OTR']]
            df2 = df[['PEKERJAAN', 'OBJECT', 'TENOR', 'OTR']]

            df2['TENOR'] = df2['TENOR'].astype(str)

            # dataAkhir = pd.DataFrame(df['cluster'].value_counts())
            # labelPekerjaan = pd.DataFrame(data = df[['PEKERJAAN']].groupby(['PEKERJAAN']).sum().sort_values(by='PEKERJAAN', ascending=False)).reset_index()
            # totalPekerjaan = pd.DataFrame(data = df['PEKERJAAN'].value_counts(sort=False).tolist(), columns=['total'])

        input_n_cluster = FormField(request.POST)
        if input_n_cluster.is_valid():
            input_n_cluster = int(request.POST.get('jumlah_cluster'))

            cost = []
        
            for num_clusters in range(1,input_n_cluster+1):
                kproto = KPrototypes(n_clusters=num_clusters, init='random', verbose=2, n_jobs=-1, n_init=5, max_iter=5)
                kproto.fit_predict(df, categorical=[0,1,2,3])
                cost.append(kproto.cost_)


            n_cluster = []
            for i in range(1,input_n_cluster+1):
                n_cluster.append(i)

            form_field = FormField()

            context = {
                'n_cost' : cost,
                'n_cluster' : n_cluster,
                'form_field' : form_field,
                }

            # return HttpResponseRedirect('/elbow-graph/', context)
            return render(request, 'elbow_graph.html', context)

    else:
        form = UploadFileForm()

    return render(request, 'elbow_graph.html', context)

#  def elbowGraph(request):

    
#     files_ = os.path.join(settings.BASE_DIR, 'media\\'+request.session.get('file'))
#     df = pd.read_excel(files_)

#     df = df[['KABUPATEN', 'PEKERJAAN', 'OBJECT', 'TENOR', 'OTR']]
#     df2 = df[['PEKERJAAN', 'OBJECT', 'TENOR', 'OTR']]

#     df2['TENOR'] = df2['TENOR'].astype(str)

#     # dataAkhir = pd.DataFrame(df['cluster'].value_counts())
#     # labelPekerjaan = pd.DataFrame(data = df[['PEKERJAAN']].groupby(['PEKERJAAN']).sum().sort_values(by='PEKERJAAN', ascending=False)).reset_index()
#     # totalPekerjaan = pd.DataFrame(data = df['PEKERJAAN'].value_counts(sort=False).tolist(), columns=['total'])


#     cost = []
#     # for i in range(1,8):
#     #     a = random.randint(1,20)
#     #     cost.append(a)
#     for num_clusters in list(range(1,6)):
#         kproto = KPrototypes(n_clusters=num_clusters, init='Cao', verbose=2)
#         kproto.fit_predict(df2, categorical=[0,1,2])
#         cost.append(kproto.cost_)

#     n_cluster = []
#     for i in range(1,6):
#         n_cluster.append(i)

#     form_field = FormField()

#     context = {
#         'n_cost' : cost,
#         'n_cluster' : n_cluster,
#         'form_field' : form_field,
#         }

#     return render(request, 'elbow_graph.html', context)

def dataJson(request):

    files_ = os.path.join(settings.BASE_DIR, 'media\\'+request.session.get('file'))
    df = pd.read_excel(files_)
    df2 = df[['ID','KABUPATEN', 'PEKERJAAN', 'OBJECT', 'TENOR' ,'OTR']].astype(str)
    df2['TENOR'] = df2['TENOR'] + str(' Bulan')
    cluster = datafarame()
    cluster = (cluster+1).astype(str)
    df2['cluster'] = cluster

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
