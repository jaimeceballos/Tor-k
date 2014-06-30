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
    url(r'^ofertas/(?P<id_oferta>\d+)/$', edit_ofertas, name='edit_ofertas'),
    url(r'^oferta/(?P<id_oferta>\d+)/$', borrar_oferta, name='borrar_oferta'),
    url(r'^producto/ver/(?P<id_prod>\d+)/$', ver_producto, name='ver_producto'),
    url(r'^micarrito/$', ver_carrito, name='ver_carrito'),
    url(r'^micarrito/remove/(?P<id_prod>\d+)/$', remove_from_cart, name='remove_from_cart'),
    url(r'^procesarpedido/$', procesar_pedido, name='procesar_pedido'),
    url(r'^procesarpedido/(?P<id_prod>\d+)/$', procesar_pedido_producto, name='procesar_pedido_producto'),
    url(r'^procesarpedido/confirmar/$', confirmar_pedido, name='confirmar_pedido'),
    url(r'^procesarpedido/cancelar/$', cancelar_pedido, name='cancelar_pedido'),
    url(r'^mispedidos/$', mis_pedidos, name='mis_pedidos'),
    url(r'^gestionpedidos/$', gestion_pedidos, name='gestion_pedidos'),
    url(r'^procesapedido/(?P<id_pedido>\d+)/$', procesa_pedido, name='procesa_pedido'),

    
	
)