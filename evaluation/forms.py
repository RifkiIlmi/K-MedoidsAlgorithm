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
        ('2018','2018'), 
        ('2019','2019'), 
      )
   ),
)

VMETHOD = (
  ('Choose',
      (
        ('-','-'),
        ('dbi','Davies-Bouldin Index Performance'),
      )
   ),
)

class EvaluationForm(forms.Form):
    tahun = forms.ChoiceField(widget=forms.Select(attrs={'id':'tahun','class':'form-control'}), choices=TAHUN)
    vmethod = forms.ChoiceField(widget=forms.Select(attrs={'id':'vmethod','class':'form-control'}), choices=VMETHOD)
    iter = forms.CharField(widget=forms.NumberInput(attrs={'id':'iters','min':3,'max':20,'class':'form-control'}))


        