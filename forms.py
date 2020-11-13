from django import forms

class getAppID(forms.Form):
    your_name = forms.CharField(label='app_ID:', max_length=50)