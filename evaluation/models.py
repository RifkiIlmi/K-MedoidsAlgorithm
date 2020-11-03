from django.db import models

# Create your models here.
from django.db import models
from preprocessing.models import ProsesKDD
from datamining.models import KMedoids 
# Create your models here.

class Evaluation(models.Model):
    best_clusters = models.CharField(max_length=225)
    tahun = models.CharField(max_length=20)

    # def __str__(self):
    #     return self.nama_bank
    
    class Meta:
        db_table = "evaluation"