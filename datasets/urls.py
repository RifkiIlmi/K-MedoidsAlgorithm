from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='datasetsIndex'),
    path('exportData/', export_data, name = "exportData"), 
    path('importData/', import_data, name = "importData"),
    path('statistics/<str:year>', statistics, name = "statistics"),
    path('resetData/<str:year>', resetData, name = "resetData"),
]