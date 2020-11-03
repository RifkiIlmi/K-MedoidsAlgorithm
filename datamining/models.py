from django.db import models
from preprocessing.models import ProsesKDD
# Create your models here.

class KMedoids(models.Model):
    rasio_k_p = models.ForeignKey(ProsesKDD, on_delete=models.CASCADE)
    cluster = models.CharField(max_length=50)

    # def __str__(self):
    #     return self.nama_bank
    
    class Meta:
        db_table = "kmedoids"