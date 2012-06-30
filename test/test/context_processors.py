from django.conf import settings as param

def settings(request):
    return {'settings' : param}
