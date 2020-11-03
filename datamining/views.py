from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, HttpResponseRedirect
from django.http import JsonResponse
from tablib import Dataset
from django.contrib import messages

import pandas as pd
import numpy as np
from .k_medoids import k_medoids

from .forms import DataMiningForm

from preprocessing.models import ProsesKDD
from .models import KMedoids

def index(request, year=0):

    key =  request.POST.get('filter-key')
    datasets_filter = KMedoids.objects.filter(rasio_k_p_id__rasio_k_id__tahun = key)

    context = {
        'year' : key,
        'data' : datasets_filter,
        'form' : DataMiningForm,
        'name': 'datamining',
        'title' : 'Data Mining - Mining Apps'
    }
    return render(request,'datamining/index.html', context)

def kmedoids(data,klaster):
    XD = data.iloc[:,2:8]
    XY = XD.astype(np.float)
    X = XY[['car','npl','roa','roe','nim','ldr']].to_numpy()
    model=k_medoids(k=klaster)
    # print('Centers found by your model:')
    centers = model.fit(X)

    label = model.predict(X)
    
    result = {
        'centers' : centers,
        'label' : label 
    }

    return result

def save(data):
    # print('true')
    # print(data.head(20))
    for list in data.itertuples():
            list = KMedoids.objects.create(
                cluster=list.cluster,
                rasio_k_p_id=list.id,
            )

def update(data):
    # print('flase')
     # print(data.head(20))
    for list in data.itertuples():
            list = KMedoids.objects.filter(rasio_k_p_id=list.id).update(
                cluster=list.cluster,
            )

def mining(request):
    form = DataMiningForm(request.POST)
    
    if form.is_valid():
        tahun = request.POST['tahun']
        method = request.POST['method']
        klaster = int(request.POST['klaster'])

        # baca dan convert data ke pandas dataframe
        rowData = ProsesKDD.objects.filter(rasio_k_id__tahun = tahun).filter(status = 'Transformed')
        preData = pd.DataFrame(list(rowData.values()))

        cekStatusData = ProsesKDD.objects.filter(rasio_k_id__tahun = tahun).filter(status = 'mining').count()

        cekData = ProsesKDD.objects.filter(rasio_k_id__tahun = tahun).count()

        cekClustered = KMedoids.objects.filter(rasio_k_p_id__rasio_k_id__tahun = tahun).filter(rasio_k_p_id__rasio_k_id__nama_bank = 'PT. BANK BNI SYARIAH').exists()

        # print(cekClustered)

        if tahun == '-' or method == '-':
            messages.add_message(request, messages.WARNING, 'Choose Your Option')
        elif cekStatusData > 0 :
            messages.add_message(request, messages.WARNING, 'Data Has Been Mined')
        elif cekData <= 0 :
            messages.add_message(request, messages.WARNING, 'No Data')
        else:
            messages.add_message(request, messages.SUCCESS, 'Data Mining Success')
            
            result = kmedoids(preData,klaster)
            preData['cluster'] = result['label']

            if cekClustered == False:
                save(preData)
            else:
                update(preData)
                
        # print(result['centers'])
    else:
        messages.add_message(request, messages.ERRROR, 'Error')
        return HttpResponseRedirect('/')

    return redirect('daminIndex', year=tahun)

def summaryProcess(request, year): 
    # print(year)
    if request.is_ajax and request.method == "GET":

        cek = KMedoids.objects.filter(rasio_k_p_id__rasio_k_id__tahun = year).count()

        # print(cek)
 
        if cek > 0:
            dat = KMedoids.objects.filter(rasio_k_p_id__rasio_k_id__tahun = year)
            # print(dat.values('rasio_k_p_id__rasio_k_id__nama_bank'))
            df = pd.DataFrame(list(dat.values(
                'rasio_k_p_id__rasio_k_id__nama_bank',
                'rasio_k_p_id__rasio_k_id__car',
                'rasio_k_p_id__rasio_k_id__npl',
                'rasio_k_p_id__rasio_k_id__roa',
                'rasio_k_p_id__rasio_k_id__roe',
                'rasio_k_p_id__rasio_k_id__nim',
                'rasio_k_p_id__rasio_k_id__ldr',
                'cluster',
            )))
            df[['rasio_k_p_id__rasio_k_id__car', 'rasio_k_p_id__rasio_k_id__npl','rasio_k_p_id__rasio_k_id__roa','rasio_k_p_id__rasio_k_id__roe','rasio_k_p_id__rasio_k_id__nim','rasio_k_p_id__rasio_k_id__ldr']] = df[['rasio_k_p_id__rasio_k_id__car', 'rasio_k_p_id__rasio_k_id__npl','rasio_k_p_id__rasio_k_id__roa','rasio_k_p_id__rasio_k_id__roe','rasio_k_p_id__rasio_k_id__nim','rasio_k_p_id__rasio_k_id__ldr']].apply(pd.to_numeric)

            # print(df)

            groupCount = df.groupby(['cluster']).count()
            groupCount = groupCount['rasio_k_p_id__rasio_k_id__nama_bank'].to_dict()
            groupCount = dict(("cluster_{}".format(k),v) for k,v in groupCount.items())

            groupMean = df.groupby(['cluster'])[['rasio_k_p_id__rasio_k_id__car',
                'rasio_k_p_id__rasio_k_id__npl',
                'rasio_k_p_id__rasio_k_id__roa',
                'rasio_k_p_id__rasio_k_id__roe',
                'rasio_k_p_id__rasio_k_id__nim',
                'rasio_k_p_id__rasio_k_id__ldr']].mean()
            groupMean = groupMean.to_dict()
            # groupMean = dict(("cluster_{}".format(k),v) for k,v in groupMean.items())
            # print(groupMean)

            data = {'status':1,'message':'Success','count':groupCount,'mean':groupMean}
            return JsonResponse({'data': data}, status=200)
        else:
            data = {'status':0,'message':'No Data / Unfiltered'}
            # print(data)
            return JsonResponse({'data': data}, status=200)
    else:
        data = {'status':9,'message':'Error'}
        # print(data)
        return JsonResponse({'data': data}, status=200)

    return JsonResponse({}, status = 400)