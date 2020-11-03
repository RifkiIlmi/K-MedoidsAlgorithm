from django import forms

TAHUN = (
  ('Choose',
      (
        ('-','-'),
        ('2012','2012'),
        ('2013','2013'),
        ('2014','2014'),
        ('2015','2015'), 
        ('2016','2016'), 
        ('2017','2017'), 
      )
   ),
)

METHOD = (
  ('Choose',
      (
        ('-','-'),
        ('kmedoids','K-Medoids'),
      )
   ),
)

class DataMiningForm(forms.Form):
    tahun = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), choices=TAHUN)
    method = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), choices=METHOD)
    klaster = forms.CharField(widget=forms.NumberInput(attrs={'min':2,'max':15,'class':'form-control'}))


        