from django.forms import ModelForm, Textarea
from django.contrib.admin.widgets import AdminDateWidget
from models import MyProfile

class ChangeForm(ModelForm):
    class Meta:
        model = MyProfile
        fields = ['first_name','last_name','birthday','biography','contacts']
        fields.reverse()
        widgets = {
            'birthday': AdminDateWidget(),
            'biography': Textarea(attrs={'cols': 40, 'rows': 10}),
            'contacts': Textarea(attrs={'cols': 40, 'rows': 5}),
        }
