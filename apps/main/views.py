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

from django.views.decorators.cache import cache_control
# Create your views here.

@login_required
def categorias(request):
	categoria = CategoriaForm()
	categorias = Categoria.objects.all()
	if request.method == 'POST':
		categoria = CategoriaForm(request.POST)
		if categoria.is_valid():
			categoria.save()
			categoria=CategoriaForm()

	print categoria
	values={
		'categoria':categoria,
		'categorias':categorias,
	}

	return render_to_response('intranet/categorias.html',values, context_instance = RequestContext(request))


@login_required
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
def edit_ofertas(request,id_oferta):
	print 'entra'
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
def obtener_productos(request,id_cat):
	data = request.POST
	productos = Producto.objects.filter(categoria = id_cat)
	data = serializers.serialize("json", productos)
	return HttpResponse(data, mimetype='application/json')