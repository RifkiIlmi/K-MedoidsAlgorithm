from import_export import resources
from .models import RasioKeuangan

class RasioKeuanganResource(resources.ModelResource):
    class Meta:
        model = RasioKeuangan