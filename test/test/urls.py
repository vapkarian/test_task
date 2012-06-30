from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth.views import login, logout
admin.autodiscover()

urlpatterns = patterns('',
                       url(r'^admin/',include(admin.site.urls)),
                       url(r'^my_admin/jsi18n',
                           'django.views.i18n.javascript_catalog'),
                       url(r'^my_admin/jsi18n',
                           'django.views.i18n.javascript_catalog'),
                       url(r'^accounts/edit/$','myprofile.views.change'),
                       url(r'^accounts/login/$',login),
                       url(r'^accounts/logout/$',logout),
                       url(r'^static/(?P<path>.*)$',
                           'django.views.static.serve',
                           {'document_root': settings.STATIC_ROOT,}),
                       url(r'^$','test.views.index'),
)
