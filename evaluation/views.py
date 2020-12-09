from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse, HttpResponseRedirect
from tablib import Dataset
from django.contrib import messages

from sklearn.metrics import davies_bouldin_score 
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

from .forms import EvaluationForm

from preprocessing.models import ProsesKDD
from datamining.models import KMedoids
from .models import Evaluation

from  datamining.k_medoids import k_medoids

def index(request):
    
    datasets_filter = Evaluation.objects.all().order_by('tahun')
    searchItem = ProsesKDD.objects.select_related('rasio_k').values_list('rasio_k__nama_bank', flat=True)
    
    context = {
        'data': datasets_filter,
        'lists': set(searchItem),
        'form' : EvaluationForm,
        'name': 'evaluation',
        'title' : 'Evaluation - Mining Apps'
    }
    return render(request,'evaluation/index.html', context)

# def dbi(data, iters):
#     XD = data.iloc[:,2:8]
#     XY = XD.astype(np.float)
#     X = XY[['car','npl','roa','roe','nim','ldr']].to_numpy()

#     best = {}
#     for it in range(iters):
#         dbi =[]
#         for i in range(2, 9):
#             kmedoidsValidityByDBI = k_medoids(k=i)
#             kmedoidsValidityByDBI.fit(X)
#             labels = kmedoidsValidityByDBI.predict(X)
#             dbi.append(davies_bouldin_score(X, labels))
#         minimum = min(dbi)
#         minBest = dbi.index(minimum)+2
#         key = 'k_'+ str(minBest) +'_iter_'+ str(it)
#         best[key] = minimum

#     return best

def dbi(data, iters):
    XD = data.iloc[:,2:8]
    XY = XD.astype(np.float)
    X = XY[['car','npl','roa','roe','nim','ldr']].to_numpy()

    dbi = {}
    for i in range(2, iters+1):
        kmedoidsValidityByDBI = k_medoids(k=i)
        kmedoidsValidityByDBI.fit(X)
        labels = kmedoidsValidityByDBI.predict(X)
        dbi['k'+str(i)] = round(davies_bouldin_score(X, labels),3)
    
    return dbi

def evaluate(request):
    """
    Evaluasi menggunakan DBI
    """
    if request.is_ajax():

        tahun = request.POST.get('tahun', None) # getting data from input tahun 
        vmethod = request.POST.get('vmethod', None) # getting data from input vmethod 
        iters = request.POST.get('iters', None) # getting data from input iters 

        cekEvaluasi = Evaluation.objects.filter(tahun = tahun).count()

        # baca dan convert data ke pandas dataframe
        rowData = ProsesKDD.objects.filter(rasio_k_id__tahun = tahun).filter(status = 'Transformed')
        preData = pd.DataFrame(list(rowData.values()))

        cekData = ProsesKDD.objects.filter(rasio_k_id__tahun = tahun).count()

        if tahun == '-' or vmethod == '-':
            alert = "warning"
            message = "Choose Your Option"
        elif cekEvaluasi > 0 :
            alert = "warning"
            message = "Tahun Data sudah dievaluasi"
        elif cekData <= 0 :
            alert = "warning"
            message = "No Data"
        else:
            alert = "success"
            message = "Evaluation Success"
        
            result = dbi(preData,int(iters))

            # print(result)
            dataku = Evaluation(
                best_clusters = result,
                tahun = tahun,
            )
            dataku.save()

        response = {
            'alert': alert,
            'message': message,
            'tahun' : tahun,
            # 'result': arrRes,
        }
        return JsonResponse(response) # return response as JSON

def search(request, keyword):
    bank = KMedoids.objects.filter(rasio_k_p__rasio_k__nama_bank=keyword).order_by('rasio_k_p__rasio_k__tahun')

    context = {
        'data' : bank,
        'namaBank': keyword,
        'name': 'evaluation',
        'title' : 'Detail Bank Evaluation - Mining Apps'
    }

    return render(request,'evaluation/detail.html', context)

def searchDetail(request):
    if request.is_ajax and request.method == "GET":
        
        tahun = request.GET.get('tahun', None) 
        namabank = request.GET.get('namabank', None) 
        cluster = request.GET.get('cluster', None) 

        dataShow = KMedoids.objects.filter(rasio_k_p_id__rasio_k_id__tahun = tahun).filter(cluster = cluster)
        df = pd.DataFrame(list(dataShow.values(
                'rasio_k_p_id__rasio_k_id__car',
                'rasio_k_p_id__rasio_k_id__npl',
                'rasio_k_p_id__rasio_k_id__roa',
                'rasio_k_p_id__rasio_k_id__roe',
                'rasio_k_p_id__rasio_k_id__nim',
                'rasio_k_p_id__rasio_k_id__ldr',
            )))
        
        dfMean = df.mean()

        car = dfMean.rasio_k_p_id__rasio_k_id__car
        npl = dfMean.rasio_k_p_id__rasio_k_id__npl
        roa = dfMean.rasio_k_p_id__rasio_k_id__roa
        roe = dfMean.rasio_k_p_id__rasio_k_id__roe
        nim = dfMean.rasio_k_p_id__rasio_k_id__nim
        ldr = dfMean.rasio_k_p_id__rasio_k_id__ldr

        data = {'status':1,'message':'Success','tahun':tahun,'cluster':cluster,'car':car,'npl':npl,'roa':roa,'roe':roe,'nim':nim,'ldr':ldr,}
        # print(data)
        return JsonResponse(data, status=200)
    else:
        data = {'status':9,'message':'Error'}
        # print(data)
        return JsonResponse(data, status=200)

    return JsonResponse({}, status = 400)