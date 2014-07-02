#! /usr/bin/python
# -*- encoding: utf-8 -*-

from django.conf.urls import patterns, include, url
from django.contrib import admin
from views import *

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', pagina_inicio,name='inicio'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^main/', include('apps.main.urls')),
    url(r'^registro/$', registro, name='registro'),
    url(r'^edit_profile/$', edit_profile, name='edit_profile'),
    url(r'^logout/$', logout, name='logout'),
    url(r'^login/$', login, name='login'),
	
)
