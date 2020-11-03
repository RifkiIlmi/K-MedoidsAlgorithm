from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, HttpResponseRedirect
from tablib import Dataset
from django.contrib import messages

import numpy as np
from numpy import nan
import pandas as pd
from sklearn import preprocessing
from sklearn.impute import SimpleImputer

from .forms import PreprocessingForm

from .models import RasioKeuangan
from .models import ProsesKDD

def index(request, year=2012):
    
    if request.method == 'POST':
        key =  request.POST.get('filter-key')
        datasets_filter = ProsesKDD.objects.filter(rasio_k_id__tahun = key)

        context = {
            'data' : datasets_filter,
            'year' : key,
            'name': 'preprocessing',
            'title' : 'Pre-Processing - Mining Apps',
            'form' : PreprocessingForm
        }
        return render(request,'preprocessing/index.html', context)
    else:
        datasets_filter = ProsesKDD.objects.filter(rasio_k_id__tahun = year)

        context = {
            'year' : year,
            'data' : datasets_filter,
            'name': 'preprocessing',
            'title' : 'Pre-Processing - Mining Apps',
            'form' : PreprocessingForm
        }
        return render(request,'preprocessing/index.html', context)

def duplicateCheck(data):
    cleaned = data.drop_duplicates(subset ="nama_bank", keep ='first', inplace=False)
    return cleaned

def missingCheck(data,strategy):
    imputer = SimpleImputer(missing_values=nan, strategy=strategy)
    imputer = imputer.fit(data.iloc[:,3:])
    data.iloc[:,3:] = imputer.transform(data.iloc[:,3:])
    return data

def bulkSave(data):
    
    # print(data.head(20))
    for list in data.itertuples():
            list = ProsesKDD.objects.create(
                car=list.car,
                npl=list.npl,
                roa=list.roa,
                roe=list.roe,
                nim=list.nim,
                ldr=list.ldr,
                rasio_k_id=list.id,
                status='Processed'
            )

def process(request):
    form = PreprocessingForm(request.POST)

    if form.is_valid():
        tahun = request.POST['tahun']
        duplicate = request.POST['duplicate']
        missing = request.POST['missing']

        # baca dan convert data ke pandas dataframe
        rowData = RasioKeuangan.objects.filter(tahun = tahun)
        duplicateData = pd.DataFrame(list(rowData.values()))

        cekStatusData = ProsesKDD.objects.filter(rasio_k_id__tahun = tahun).filter(status = 'Processed').count()
        cekStatusTra = ProsesKDD.objects.filter(rasio_k_id__tahun = tahun).filter(status = 'Transformed').count()
        cekData = RasioKeuangan.objects.filter(tahun = tahun).count()
        
        if tahun == '-' or duplicate == '-' or missing == '-':
            messages.add_message(request, messages.WARNING, 'Choose Your Option')
        elif cekStatusData > 0 or cekStatusTra>0 :
            messages.add_message(request, messages.WARNING, 'Data Has Been Proocessed Or Transformed')
        elif cekData <= 0 :
            messages.add_message(request, messages.WARNING, 'No Data')
        else:
            # bagi data persen /100 agar normal
            duplicateData[['car','npl','roa','roe','nim','ldr']] = duplicateData[['car','npl','roa','roe','nim','ldr']].div(100)

            if duplicate == '1':
                duplicateData = duplicateCheck(duplicateData)
            else:
                duplicateData

            missingData = missingCheck(duplicateData, missing)
            
            bulkSave(missingData)
            messages.add_message(request, messages.SUCCESS, 'Data Processing Success')

            # print(missingData)
    else:
        return HttpResponseRedirect('/')

    return redirect('preprocessingIndex', year=tahun)