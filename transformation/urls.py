from django.urls import path
from .views import index, transform

urlpatterns = [
    path('', index, name='transformationIndex'),
    path('<year>/', index, name='transformationIndex'),
    path('transform', transform, name='transform'),
] 