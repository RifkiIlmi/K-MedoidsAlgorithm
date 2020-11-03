from django.shortcuts import render, redirect
from django.shortcuts import HttpResponse
from django.contrib import messages


def index(request):
    context = {
        'name':'home',
        'title' : 'Mining Apps'
    }
    return render(request,'home/index.html', context)