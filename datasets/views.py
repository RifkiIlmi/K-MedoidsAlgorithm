from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from tablib import Dataset
from django.contrib import messages
import datetime

import numpy as np
import pandas as pd

from .resources import RasioKeuanganResource
from .models import RasioKeuangan

def index(request,):
    nowDate = datetime.datetime.now()
    year = nowDate.year - 8

    if request.method == 'POST':
        key =  request.POST.get('filter-key')
        datasets_filter = RasioKeuangan.objects.filter(tahun = key)

        context = {
            'data' : datasets_filter,
            'year' : key,
            'name': 'datasets',
            'title' : 'Datasets - Mining Apps'
        }
        return render(request,'datasets/index.html', context)
    else:
        datasets_filter = RasioKeuangan.objects.filter(tahun = year)

        context = {
            'data' : datasets_filter,
            'year' : year,
            'name': 'datasets',
            'title' : 'Datasets - Mining Apps'
        }
        return render(request,'datasets/index.html', context)
 
def export_data(request):
    if request.method == 'POST':
        # Get selected option from form
        file_format = request.POST['file-format']
        rk_resource = RasioKeuanganResource()
        dataset = rk_resource.export()
        if file_format == 'CSV':
            response = HttpResponse(dataset.csv, content_type='text/csv')
            response['Content-Disposition'] = 'attachment; filename="exported_data.csv"'
            messages.add_message(request, messages.SUCCESS, 'Success Export Data CSV')
            return response        
        elif file_format == 'JSON':
            response = HttpResponse(dataset.json, content_type='application/json')
            response['Content-Disposition'] = 'attachment; filename="exported_data.json"'
            messages.add_message(request, messages.SUCCESS, 'Success Export Data JSON')
            return response
        elif file_format == 'XLSX (Excel)':
            response = HttpResponse(dataset.xlsx, content_type='application/vnd.ms-excel')
            response['Content-Disposition'] = 'attachment; filename="exported_data.xlsx"'
            messages.add_message(request, messages.SUCCESS, 'Success Export Data EXCEL')
            return response

    return redirect('datasetsIndex')

def import_data(request):
    if request.method == 'POST':
        file_format = request.POST['file-format']
        rk_resource = RasioKeuanganResource()
        dataset = Dataset()
        new_rasioKeuangan = request.FILES['importData']
 
        if file_format == 'CSV':
            imported_data = dataset.load(new_rasioKeuangan.read().decode('utf-8'),format='csv')
            result = rk_resource.import_data(dataset, dry_run=True)
            messages.add_message(request, messages.SUCCESS, 'Success Import Data CSV')
        elif file_format == 'JSON':
            imported_data = dataset.load(new_rasioKeuangan.read().decode('utf-8'),format='json')
            # Testing data import
            result = rk_resource.import_data(dataset, dry_run=True)
            messages.add_message(request, messages.SUCCESS, 'Success Import Data JSON')
        elif file_format == 'EXCEL':
            imported_data = dataset.load(new_rasioKeuangan.read(), format='xlsx')
            # Testing data import
            result = rk_resource.import_data(dataset, dry_run=True)
            messages.add_message(request, messages.SUCCESS, 'Success Import Data EXCEL')

        if not result.has_errors():
            # Import now
            rk_resource.import_data(dataset, dry_run=False)

    return redirect('datasetsIndex')     

def statistics(request, year): 
    # print(year) 
    if request.is_ajax and request.method == "GET":

        df = pd.DataFrame(list(RasioKeuangan.objects.filter(tahun = year).values()))

        # print(len(df.index))
 
        if len(df.index) > 0:
            df.drop(['id'], axis=1)
            df[['car', 'npl','roa','roe','nim','ldr']] = df[['car', 'npl','roa','roe','nim','ldr']].apply(pd.to_numeric)

            mv = df.isnull().sum()
            # print(mv)
            missing_values = mv.to_dict()
            desc = df.describe().to_dict()
            duplicate = df[df.duplicated(['nama_bank'])].to_dict()
            # print(duplicate['nama_bank'])
            data = {'status':1,'message':'Success','missing_values':missing_values, 'describe':desc,'duplicate':duplicate['nama_bank']}
            # print(data)
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