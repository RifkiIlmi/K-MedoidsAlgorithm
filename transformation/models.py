from django.db import models

# Create your models here.

# class Transformation(models.Model):
#     trans_id = models.AutoField(primary_key=True)
#     nama_bank = models.CharField(max_length=150)
#     tahun = models.CharField(max_length=10)
#     car = models.DecimalField(max_digits=19, decimal_places=10)
#     npl = models.DecimalField(max_digits=19, decimal_places=10)
#     roa = models.DecimalField(max_digits=19, decimal_places=10)
#     roe = models.DecimalField(max_digits=19, decimal_places=10)
#     nim = models.DecimalField(max_digits=19, decimal_places=10)
#     ldr = models.DecimalField(max_digits=19, decimal_places=10)

#     def __str__(self):
#         return self.nama_bank
    
#     class Meta:
#         db_table = "transformation"