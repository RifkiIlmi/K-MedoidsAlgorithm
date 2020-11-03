from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, HttpResponseRedirect
from tablib import Dataset
from django.contrib import messages

from .forms import TransformationForm

import numpy as np
from numpy import nan
import pandas as pd
from sklearn import preprocessing
from sklearn.impute import SimpleImputer

from preprocessing.models import ProsesKDD

def index(request, year=2012):

    if request.method == 'POST':
        key =  request.POST.get('filter-key')
        datasets_filter = ProsesKDD.objects.filter(rasio_k_id__tahun = key).filter(status = 'Transformed')

        context = {
            'data' : datasets_filter,
            'name': 'transformation',
            'year' : key,
            'title' : 'Transformation - Mining Apps',
            'form' : TransformationForm
        }
        return render(request,'transformation/index.html', context)
    else:
        datasets_filter = ProsesKDD.objects.filter(rasio_k_id__tahun = year).filter(status = 'Transformed')

        context = {
            'data' : datasets_filter,
            'name': 'transformation',
            'year' : year,
            'title' : 'Transformation - Mining Apps',
            'form' : TransformationForm
        }
        return render(request,'transformation/index.html', context)
        

def minmax_norm(data):
    data.iloc[:,2:8] = data.iloc[:,2:8].values #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(data.iloc[:,2:8])
    data.iloc[:,2:8] = pd.DataFrame(x_scaled,columns=['car','npl','roa','roe','nim','ldr'])

    return data 

def bulkUpdate(data):
    
    # print(data.head(20))
    for list in data.itertuples():
            list = ProsesKDD.objects.filter(id=list.id).update(
                car=list.car,
                npl=list.npl,
                roa=list.roa,
                roe=list.roe,
                nim=list.nim,
                ldr=list.ldr,
                status='Transformed'
            )


def transform(request):
    form = TransformationForm(request.POST)

    if form.is_valid():
        tahun = request.POST['tahun']
        normalization = request.POST['normalization']

        # baca dan convert data ke pandas dataframe
        rowData = ProsesKDD.objects.filter(rasio_k_id__tahun = tahun).filter(status = 'Processed')
        preTransData = pd.DataFrame(list(rowData.values()))

        cekStatusData = ProsesKDD.objects.filter(rasio_k_id__tahun = tahun).filter(status = 'Transformed').count()

        cekData = ProsesKDD.objects.filter(rasio_k_id__tahun = tahun).count()

        if tahun == '-' or normalization == '-':
            messages.add_message(request, messages.WARNING, 'Choose Your Option')
        elif cekStatusData > 0 :
            messages.add_message(request, messages.WARNING, 'Data Has Been Transformed')
        elif cekData <= 0 :
            messages.add_message(request, messages.WARNING, 'No Data')
        else: 

            predata = minmax_norm(preTransData)
            # print(predata)
            bulkUpdate(predata)

            messages.add_message(request, messages.SUCCESS, 'Data Transform Success')

        # print(preTransData,cekData,cekStatusData)
    else:
        return HttpResponseRedirect('/')

    return redirect('transformationIndex', year=tahun)
