from django import forms

#not sure how this works or if i even need this... 
#need templates to work to test out how this works.
class Input(forms.Form):
    input = forms.CharField(label="input", max_length=250)
