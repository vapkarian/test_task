from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/', include(admin.site.urls)),
                       (r'^accounts/login/$',  login),
                       (r'^accounts/logout/$', logout),
                       url(r'^$','test.views.index'),
)
