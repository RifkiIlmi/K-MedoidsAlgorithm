from django.urls import path
from .views import index, process

urlpatterns = [
    path('<year>/', index, name='preprocessingIndex'),
    path('', index, name='preprocessingIndex'),
    path('processing', process, name='processing'),
]