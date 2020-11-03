from django.urls import path
from .views import index, mining, summaryProcess

urlpatterns = [
    path('', index, name='daminIndex'), 
    path('<year>/', index, name='daminIndex'), 
    path('mining', mining, name='mining'),
    path('summaryProcess/<str:year>', summaryProcess, name = "summaryProcess"),
] 