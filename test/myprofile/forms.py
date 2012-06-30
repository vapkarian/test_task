from django import forms
from django.contrib.admin.widgets import AdminDateWidget

class ChangeForm(forms.Form):
    first_name = forms.CharField(max_length=35)
    last_name = forms.CharField(max_length=50)
    birthday = forms.DateField(required=False,widget=AdminDateWidget())
    biography = forms.CharField(max_length=3000,
                                required=False,widget=forms.Textarea)
    contacts = forms.CharField(max_length=500,
                               required=False,widget=forms.Textarea)
