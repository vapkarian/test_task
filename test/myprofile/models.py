from django.db import models
from django.contrib.auth.models import User

class MyProfile(models.Model):
    user = models.OneToOneField(User,unique=True,related_name='profile')
    first_name = models.CharField(max_length=35)
    last_name = models.CharField(max_length=50)
    birthday = models.DateField(blank=True, null=True)
    biography = models.CharField(max_length=3000, blank=True)
    contacts = models.CharField(max_length=500, blank=True)
    def __unicode__(self):
        return '%s %s' % (self.first_name, self.last_name)

