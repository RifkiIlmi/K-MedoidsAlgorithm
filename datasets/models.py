from django.db import models

# Create your models here.

class RasioKeuangan(models.Model):
    nama_bank = models.CharField(max_length=150)
    tahun = models.CharField(max_length=10)
    car = models.DecimalField(max_digits=19, decimal_places=4)
    npl = models.DecimalField(max_digits=19, decimal_places=4)
    roa = models.DecimalField(max_digits=19, decimal_places=4)
    roe = models.DecimalField(max_digits=19, decimal_places=4)
    nim = models.DecimalField(max_digits=19, decimal_places=4)
    ldr = models.DecimalField(max_digits=19, decimal_places=4)

    def __str__(self):
        return self.nama_bank
    
    class Meta:
        db_table = "data_rasio_keuangan"