from django.http import HttpResponseRedirect
from django.template.response import TemplateResponse
from myprofile.forms import ChangeForm
from myprofile.models import MyProfile

def change(request):
    if not request.user.is_authenticated():
        return TemplateResponse(request,'registration/edit_profile.html')
    if request.method == 'POST':
        form = ChangeForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            p = MyProfile.objects.get(id=request.user.profile.id)
            p.first_name = cd['first_name']
            p.last_name = cd['last_name']
            p.birthday = cd['birthday']
            p.biography = cd['biography']
            p.contacts = cd['contacts']
            p.save()
            return HttpResponseRedirect('/')
    else:
        form = ChangeForm(initial={
            'first_name':request.user.profile.first_name,
            'last_name':request.user.profile.last_name,
            'birthday':request.user.profile.birthday,
            'biography':request.user.profile.biography,
            'contacts':request.user.profile.contacts
            }
                          )
    return TemplateResponse(request,'registration/edit_profile.html',
                            {'form':form})
