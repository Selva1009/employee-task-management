from django import forms
from .models import Emp_details 
import random as rd

class Emp_form(forms.ModelForm):
    Gender = forms.ChoiceField(choices=[('Male','Male'),('Female','Female')])
    # DOB = forms.DateField(widget=forms.DateInput(attrs={'type':'date'}))
    Emp_Id = forms.IntegerField(widget=forms.NumberInput(attrs={'value':rd.randint(100,999)}))

    class Meta:
        model = Emp_details
        exclude = ['DOJ']