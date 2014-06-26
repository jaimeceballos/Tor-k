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
	categoria = CategoriaForm(instance=Categoria.objects.get(id=id_cat))
	categorias = Categoria.objects.all()
	
	if request.method == 'POST':
		categoria = CategoriaForm(request.POST)
		if categoria.is_valid():
			cat = Categoria.objects.get(id=id_cat)
			cat.descripcion = categoria.cleaned_data['descripcion']
			cat.save()
			categoria=CategoriaForm()
			return HttpResponseRedirect(reverse('categorias'))
	values={
		'categoria':categoria,
		'categorias':categorias,
	}

	return render_to_response('intranet/categorias.html',values, context_instance = RequestContext(request))

@login_required
def productos(request):
	producto = ProductoForm()
	productos = Producto.objects.all()
	if request.method == 'POST':
		producto = ProductoForm(request.POST,request.FILES)
		if producto.is_valid():
			producto.save()
			producto = ProductoForm()

	values={
		'producto':producto,
		'productos':productos,
	}

	return render_to_response('intranet/productos.html',values, context_instance = RequestContext(request))