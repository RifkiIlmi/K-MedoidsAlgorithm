from django.urls import path
from .views import *

urlpatterns = [
    path('', index, name='evaluationIndex'),
    path('evaluate', evaluate, name='evaluate'),
    path('search/<str:keyword>', search, name='search'),
    path('searchDetail', searchDetail, name='searchDetail'),
] 