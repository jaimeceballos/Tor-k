from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    url(r'^categorias/$', categorias, name='categorias'),
    url(r'^categoria/(?P<id_cat>\d+)/$', edit_categorias, name='edit_categorias'),
    url(r'^categorias/(?P<id_cat>\d+)/$', borrar_categoria, name='borrar_categoria'),
    url(r'^productos/$', productos, name='productos'),

    
	
)