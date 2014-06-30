from django.shortcuts import render, render_to_response, get_object_or_404
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponseRedirect, HttpResponse, Http404
import datetime
from django.conf import settings
from django.template import RequestContext
from apps.main.models import *
from apps.main.forms import *
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
import simplejson
from django.core import serializers
from tork.views import productos_publicar
from django.views.decorators.cache import cache_control
# Create your views here.

@login_required
@cache_control(must_revalidate=True, max_age=3600, private=True)
def categorias(request):
	categoria = CategoriaForm()
	categorias = Categoria.objects.all()
	if request.method == 'POST':
		categoria = CategoriaForm(request.POST)
		if categoria.is_valid():
			categoria.save()
			categoria=CategoriaForm()

	values={
		'categoria':categoria,
		'categorias':categorias,
	}

	return render_to_response('intranet/categorias.html',values, context_instance = RequestContext(request))


@login_required
@cache_control(must_revalidate=True, max_age=3600, private=True)
def borrar_categoria(request, id_cat):

	categoria = get_object_or_404(Categoria, id = id_cat) 
	

	if categoria.puedo_eliminar:
		categoria.delete()
		return HttpResponseRedirect(reverse('categorias'))

 	categoria = CategoriaForm()
	categorias = Categoria.objects.all()
	values={
		'categoria':categoria,
		'categorias':categorias,
	}
 	return render_to_response('intranet/categorias.html',values, context_instance = RequestContext(request))

@login_required
@cache_control(must_revalidate=True, max_age=3600, private=True)
def edit_categorias(request,id_cat):
	cat = Categoria.objects.get(id=id_cat)
	categoria = CategoriaForm(instance=cat)
	categorias = Categoria.objects.all()
	
	if request.method == 'POST':
		categoria = CategoriaForm(request.POST)
		if categoria.is_valid():
			cat.descripcion = categoria.cleaned_data['descripcion']
			cat.save()
			categoria=CategoriaForm()
			return HttpResponseRedirect(reverse('categorias'))
	values={
		'cat':cat,
		'categoria':categoria,
		'categorias':categorias,
	}

	return render_to_response('intranet/edit_categorias.html',values, context_instance = RequestContext(request))

@login_required
@cache_control(must_revalidate=True, max_age=3600, private=True)
def productos(request):
	producto = ProductoForm()
	productos = Producto.objects.all()
	categorias = Categoria.objects.all()
	if request.method == 'POST':
		producto = ProductoForm(request.POST,request.FILES)
		if producto.is_valid():
			producto.save()
			producto = ProductoForm()

	values={
		'producto':producto,
		'productos':productos,
		'categorias':categorias,
	}

	return render_to_response('intranet/productos.html',values, context_instance = RequestContext(request))
@login_required
@cache_control(must_revalidate=True, max_age=3600, private=True)
def edit_productos(request,id_prod):
	prod = Producto.objects.get(id=id_prod)
	producto = ProductoForm()
	productos = Producto.objects.all()
	categorias = Categoria.objects.all()
	if request.method == 'POST':
		producto = ProductoForm(request.POST,request.FILES)
		if producto.is_valid():
			prod.categoria 		= producto.cleaned_data['categoria']
			prod.descripcion 	= producto.cleaned_data['descripcion']
			prod.stock_minimo 	= producto.cleaned_data['stock_minimo']
			prod.punto_reorden 	= producto.cleaned_data['punto_reorden']
			prod.stock_maximo 	= producto.cleaned_data['stock_maximo']
			prod.stock_actual 	= producto.cleaned_data['stock_actual']
			prod.costo 			= producto.cleaned_data['costo']
			if producto.cleaned_data['imagen']:
				prod.imagen 	= producto.cleaned_data['imagen']
			prod.save()
			producto = ProductoForm()
			return HttpResponseRedirect(reverse('productos'))
	producto = ProductoForm(instance=prod)
	values={
		'prod':prod,
		'producto':producto,
		'productos':productos,
		'categorias':categorias,
	}

	return render_to_response('intranet/edit_productos.html',values, context_instance = RequestContext(request))

@login_required
@cache_control(must_revalidate=True, max_age=3600, private=True)
def borrar_producto(request, id_prod):

	producto = get_object_or_404(Producto, id = id_prod) 
	
	if producto.puedo_eliminar:
		producto.delete()
		return HttpResponseRedirect(reverse('productos'))

 	producto = ProductoForm()
	productos = Producto.objects.all()
	values={
		'producto':producto,
		'productos':productos,
	}
 	return render_to_response('intranet/productos.html',values, context_instance = RequestContext(request))

@login_required
@cache_control(must_revalidate=True, max_age=3600, private=True)
def ofertas(request):
	categorias = Categoria.objects.all()
	oferta     = OfertaForm()
	ofertas	   = Oferta.objects.all()	
	if request.method == 'POST':
		oferta = OfertaForm(request.POST)
		if oferta.is_valid():
			oferta.save()
			oferta=OfertaForm()
 	values={
 		'categorias':categorias,
 		'oferta':oferta,
 		'ofertas':ofertas,
 	}
 	return render_to_response('intranet/ofertas.html',values, context_instance = RequestContext(request))

@login_required
@cache_control(must_revalidate=True, max_age=3600, private=True)
def borrar_oferta(request,id_oferta):

	oferta = get_object_or_404(Oferta, id = id_oferta)

	if oferta.puedo_eliminar:
		oferta.delete()
		return HttpResponseRedirect(reverse('ofertas'))
	categorias = Categoria.objects.all()
	oferta     = OfertaForm()
	ofertas	   = Oferta.objects.all()
	values={
 		'categorias':categorias,
 		'oferta':oferta,
 		'ofertas':ofertas,
 	}
 	return render_to_response('intranet/ofertas.html',values, context_instance = RequestContext(request))

@login_required
@cache_control(must_revalidate=True, max_age=3600, private=True)
def edit_ofertas(request,id_oferta):
	of 		   = Oferta.objects.get(id=id_oferta)
	categorias = Categoria.objects.all()
	oferta     = OfertaForm(instance=of)
	oferta.fields['categoria'].initial = of.producto.categoria
	ofertas	   = Oferta.objects.all()	
	if request.method == 'POST':
		oferta = OfertaForm(request.POST)
		if oferta.is_valid():
			of.producto = oferta.cleaned_data['producto']
			of.fecha_inicio = oferta.cleaned_data['fecha_inicio']
			of.fecha_fin	= oferta.cleaned_data['fecha_fin']
			of.costo = oferta.cleaned_data['costo']
			of.save()
			oferta=OfertaForm()
			return HttpResponseRedirect(reverse('ofertas'))
 	values={
 		'categorias':categorias,
 		'oferta':oferta,
 		'ofertas':ofertas,
 		'of':of,
 	}
 	return render_to_response('intranet/edit_ofertas.html',values, context_instance = RequestContext(request))



@login_required
@cache_control(must_revalidate=True, max_age=3600, private=True)
def obtener_productos(request,id_cat):
	data = request.POST
	productos = Producto.objects.filter(categoria = id_cat)
	data = serializers.serialize("json", productos)
	return HttpResponse(data, mimetype='application/json')

@cache_control(must_revalidate=True, max_age=3600, private=True)
def ver_producto(request,id_prod):
	form = LoginForm()
	categorias = Categoria.objects.all()
	prod = Producto.objects.get(id=id_prod)
	info=""
	if request.method == 'POST':
		if not request.user.is_authenticated():
			
			values={
				'form':form,
 				'categorias':categorias,
 				'prod':prod,
 			}
			return render_to_response('internet/must_login.html',values, context_instance = RequestContext(request))
		else:
			lista = request.session['carrito']
			if Producto.objects.get(id=id_prod) in lista:
				info = "ya se encuentra en su carrito"
			else:
				lista.append(Producto.objects.get(id=id_prod))
				request.session['carrito'] = lista
				info = "se agrego a su carrito."	
				request.session['cant'] = len(lista)
	categorias = Categoria.objects.all()
	prod = Producto.objects.get(id=id_prod)
	values={
		'info':info,
		'form':form,
 		'categorias':categorias,
 		'prod':prod,
 	}
 	return render_to_response('internet/ver_producto.html',values, context_instance = RequestContext(request))

@login_required
@cache_control(must_revalidate=True, max_age=3600, private=True)
def ver_carrito(request):
	carrito = request.session['carrito']
	productos, ofertas = productos_publicar()
	prods = []
	for producto in carrito:

		try:
			if ofertas.get(producto=producto):
				p = ofertas.get(producto=producto).producto
				p.costo = ofertas.get(producto=producto).costo
				prods.append(p)
		except:
			prods.append(producto)
	categorias = Categoria.objects.all()
	values={
		'prods':prods,
		'categorias':categorias,
 	}
 	return render_to_response('extranet/ver_carrito.html',values, context_instance = RequestContext(request))

@login_required
@cache_control(must_revalidate=True, max_age=3600, private=True)
def remove_from_cart(request,id_prod):
	carrito = request.session['carrito']
	carrito.remove(Producto.objects.get(id=id_prod))
	request.session['carrito'] = carrito
	return HttpResponseRedirect(reverse('ver_carrito'))

@login_required
@cache_control(must_revalidate=True, max_age=3600, private=True)
def procesar_pedido(request):
	if not 'pedido' in request.session:
		pedido = Pedido()
		pedido.cliente = UserProfile.objects.get(user=request.user)
		pedido.estado_pedido = EstadoPedido.objects.get(descripcion__contains='Creado')
		pedido.save()
		request.session['pedido'] = pedido
	else:
		pedido = request.session['pedido']
	categorias = Categoria.objects.all()
	values={
		'pedido':pedido,
		'categorias':categorias,
 	}
 	return render_to_response('extranet/procesar_pedido.html',values, context_instance = RequestContext(request))