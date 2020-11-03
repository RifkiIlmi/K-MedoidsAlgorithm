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
DUPLICATE = (
  ('Choose',
      (
        ('-','-'),
        ('1','Yes'),
        ('2','No'), 
      )
   ),
)
MISSING = (
  ('Choose',
      (
        ('-','-'),
        ('mean','Mean'),
        ('median','Median'),
        ('most_frequent','Most Frequent'),
      )
   ),
)

class PreprocessingForm(forms.Form):
    tahun = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), choices=TAHUN)
    duplicate = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), choices=DUPLICATE)
    missing = forms.ChoiceField(widget=forms.Select(attrs={'class':'form-control'}), choices=MISSING)


        