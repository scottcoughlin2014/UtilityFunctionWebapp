from django import forms

class Input(forms.Form):
    input = forms.CharField(label="input", max_length=250)