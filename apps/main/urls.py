from django.conf.urls import patterns, include, url
from views import *

urlpatterns = patterns('',
    url(r'^categorias/$', categorias, name='categorias'),
    url(r'^categoria/(?P<id_cat>\d+)/$', edit_categorias, name='edit_categorias'),
    url(r'^categorias/(?P<id_cat>\d+)/$', borrar_categoria, name='borrar_categoria'),
    url(r'^productos/$', productos, name='productos'),
    url(r'^productos/(?P<id_prod>\d+)/$', edit_productos, name='edit_productos'),
    url(r'^producto/(?P<id_prod>\d+)/$', borrar_producto, name='borrar_producto'),
    url(r'^ofertas/$', ofertas, name='ofertas'),
    url(r'^ofertas/prod/(?P<id_cat>\d+)/$', obtener_productos, name='obtener_productos'),

    
	
)