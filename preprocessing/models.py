from django.db import models
from datasets.models import RasioKeuangan

# Create your models here.

class ProsesKDD(models.Model):

    NOPROCESS = 'NO'
    PROCESSED = 'PR'
    TRANSFORMED = 'TR'
    MINE = 'MN'
    KKD_STATUS_CHOICES = [
        (NOPROCESS, 'No Process'),
        (PROCESSED, 'Processed'),
        (TRANSFORMED, 'Transformed')
    ]

    rasio_k = models.ForeignKey(RasioKeuangan, on_delete=models.CASCADE)
    car = models.DecimalField(max_digits=19, decimal_places=4)
    npl = models.DecimalField(max_digits=19, decimal_places=4)
    roa = models.DecimalField(max_digits=19, decimal_places=4)
    roe = models.DecimalField(max_digits=19, decimal_places=4)
    nim = models.DecimalField(max_digits=19, decimal_places=4)
    ldr = models.DecimalField(max_digits=19, decimal_places=4)
    status = models.CharField(max_length=50, choices=KKD_STATUS_CHOICES, default=NOPROCESS)

    def __str__(self):
        return self.data_id
    
    class Meta:
        db_table = "proses_kdd"