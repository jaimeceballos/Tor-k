from django.shortcuts import render, render_to_response, get_object_or_404
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponseRedirect, HttpResponse, Http404
from datetime import datetime,date
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
	print 'llega'
	if request.method == 'POST':
		producto = ProductoForm(request.POST,request.FILES)
		if producto.is_valid():
			prod.categoria 		= producto.cleaned_data['categoria']
			prod.espec 			= producto.cleaned_data['espec']
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
			elif Producto.objects.get(id=id_prod).stock_actual == 0:
				info = "temporalmente fuera de stock."
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
def remove_from_cart(request,id_prod):
	carrito = request.session['carrito']
	carrito.remove(Producto.objects.get(id=id_prod))
	request.session['carrito'] = carrito
	return HttpResponseRedirect(reverse('ver_carrito'))

@login_required
def procesar_pedido(request):
	if not 'pedido' in request.session:
		pedido = Pedido()
		pedido.cliente = UserProfile.objects.get(user=request.user)
		pedido.estado_pedido = EstadoPedido.objects.get(descripcion__contains='Creado')
		pedido.save()
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
		for producto in prods:
			prodpedido = ProductoPedido()
			prodpedido.pedido = pedido
			prodpedido.producto = producto
			prodpedido.costo = producto.costo
			prodpedido.save()

				
		request.session['pedido'] = pedido
	else:
		pedido = request.session['pedido']
	productos_pedidos = ProductoPedido.objects.filter(pedido=pedido)
	categorias = Categoria.objects.all()
	values={
		'info':'',
		'total':calcular_total_pedido(request),
		'pedido':pedido,
		'productos_pedidos':productos_pedidos,
		'categorias':categorias,
 	}
 	return render_to_response('extranet/procesar_pedido.html',values, context_instance = RequestContext(request))

@login_required
def procesar_pedido_producto(request,id_prod):
	pedido = request.session['pedido']
	productos_pedidos = ProductoPedido.objects.filter(pedido = pedido)
	categorias = Categoria.objects.all()
	form = ProductoPedidoForm()
	producto = Producto.objects.get(id = id_prod)
	info=""
	if request.method == 'POST':
		form = ProductoPedidoForm(request.POST)
		if form.is_valid():
			producto = Producto.objects.get(id=id_prod)
			cantidad_pedida = form.cleaned_data['cantidad']
			producto_pedido = productos_pedidos.get(producto=producto)
			producto_pedido.cantidad = cantidad_pedida
			producto_pedido.save()
			return HttpResponseRedirect(reverse('procesar_pedido'))
			
	values={
		'form':form,
		'producto':producto,
		'pedido':pedido,
		'productos_pedidos':productos_pedidos,
		'categorias':categorias,
 	}
 	return render_to_response('extranet/procesar_pedido_producto.html',values, context_instance = RequestContext(request))	

@login_required
def confirmar_pedido(request):
 	pedido = request.session['pedido']
 	categorias = Categoria.objects.all()
 	productos_pedidos = ProductoPedido.objects.filter(pedido=pedido)
 	info=""
 	if request.method == 'POST':
 		form = PedidoForm(request.POST)
 		if form.is_valid():
 			pedido.tipo_envio =	form.cleaned_data['tipo_envio']
 			pedido.metodo_pago = form.cleaned_data['metodo_pago']
 			pedido.save()
			del(request.session['pedido'])
			return HttpResponseRedirect('/')
 	if is_pedido_valid(request):
		pedido.estado_pedido = EstadoPedido.objects.get(descripcion__contains="Confirmado")
		pedido.save()
		request.session['carrito']=[]
		form = PedidoForm()
		values={
			'pedido':pedido,
			'form':form,
			'info':info,
			'productos_pedidos':productos_pedidos,
			'categorias':categorias,
 		}
 		return render_to_response('extranet/pedido_ok.html',values, context_instance = RequestContext(request))			
 	else:
 		info="Verifique que haya seleccionado la cantidad en cada producto pedido."
 		values={
 			'info':info,
			'total':calcular_total_pedido(request),
			'pedido':pedido,
			'productos_pedidos':productos_pedidos,
			'categorias':categorias,
 		}
 		return render_to_response('extranet/procesar_pedido.html',values, context_instance = RequestContext(request))

@login_required
def cancelar_pedido(request):
	pedido = request.session['pedido']
	productos_pedidos = ProductoPedido.objects.filter(pedido=pedido)
 	info=""
	for producto_pedido in productos_pedidos:
		producto_pedido.delete()
	pedido.delete()
	del(request.session['pedido'])
	request.session['carrito']=[]
	return HttpResponseRedirect('/')

@login_required
def mis_pedidos(request):
	categorias = Categoria.objects.all()
	pedidos = Pedido.objects.filter(cliente=request.user)
	values={	
 			'pedidos':pedidos,
			'categorias':categorias,
 		}
 	return render_to_response('extranet/mis_pedidos.html',values, context_instance = RequestContext(request))

@login_required
def gestion_pedidos(request):
	pedidos_pendientes = Pedido.objects.all()
	pedidos_pendientes = pedidos_pendientes.exclude(estado_pedido=EstadoPedido.objects.get(descripcion__contains="Finalizado"))
	values = {
		'pedidos':pedidos_pendientes,
	}

	return render_to_response('intranet/gestion_pedidos.html',values, context_instance = RequestContext(request))

@login_required
def procesa_pedido(request,id_pedido):
	pedido = Pedido.objects.get(id=id_pedido)
	productos_pedido = ProductoPedido.objects.filter(pedido=pedido)
	form = ProductoPedidoForm()
	values = {
		'form':form,
		'pedido':pedido,
		'productos_pedido':productos_pedido,
	}
	return render_to_response('intranet/procesa_pedidos.html',values,context_instance=RequestContext(request))

@login_required
def anula_item(request,id_prodpedido):
	producto_pedido = ProductoPedido.objects.get(id = id_prodpedido)
	if request.method=='POST':
		producto_pedido.observaciones = request.POST['observaciones']
		producto_pedido.anulado = True
		producto_pedido.save()	
	return HttpResponseRedirect('../../%d/' % producto_pedido.pedido.id)
	
@login_required
def modifica_item(request,id_prodpedido):
	producto_pedido = ProductoPedido.objects.get(id=id_prodpedido)
	if request.method == 'POST':
		producto_pedido.observaciones = request.POST['observaciones']
		producto_pedido.cantidad = request.POST['cantidad']
		producto_pedido.save()
	return HttpResponseRedirect('../../%d/' % producto_pedido.pedido.id)	

@login_required
def facturar_pedido(request,id_pedido):
	pedido = Pedido.objects.get(id=id_pedido)
	prods_pedido = ProductoPedido.objects.filter(pedido=id_pedido)
	prods_pedido = prods_pedido.filter(anulado=False)
	factura 	= Factura()
	if request.method == 'POST':
		fact = FacturaForm(request.POST)
		if fact.is_valid():
			factura = Factura.objects.get(pedido=pedido)
			factura.tipo = fact.cleaned_data['tipo']
			factura.save()
			pedido.estado_pedido = EstadoPedido.objects.get(descripcion__contains='Facturado')
			pedido.save()
			return HttpResponseRedirect(reverse('gestion_pedidos'))
	if pedido.estado_pedido.descripcion == 'Procesado':
		form = FacturaForm(instance=factura)
		factura = Factura.objects.get(pedido = pedido)		
		detalle = DetalleFactura.objects.filter(factura=factura)
		values = {
			'form':form,
			'factura':factura,
			'detalle':detalle,
		}
		return render_to_response('intranet/factura.html',values,context_instance=RequestContext(request))
			
	factura.pedido = pedido
	factura.cliente = UserProfile.objects.get(user=pedido.cliente)
	factura.save()
	total = 0
	for item in prods_pedido:
		detalle = DetalleFactura()
		detalle.factura = factura
		detalle.pedido_producto = item
		detalle.costo = item.costo * item.cantidad
		detalle.save()
		producto = Producto.objects.get(id = item.producto.id)
		producto.stock_actual -= item.cantidad
		producto.save()
		total += detalle.costo
	factura.total = total
	factura.save()
	detalle = DetalleFactura.objects.filter(factura=factura)
	form = FacturaForm(instance=factura)
	pedido.estado_pedido = EstadoPedido.objects.get(descripcion__contains='Procesado')
	pedido.save()
	values = {
		'form':form,
		'factura':factura,
		'detalle':detalle,
	}
	return render_to_response('intranet/factura.html',values,context_instance=RequestContext(request))
	
	
@login_required
def rechazar_pedido(request,id_pedido):
	pedido = Pedido.objects.get(id = id_pedido)
	if request.method=='POST':
		pedido.observaciones = request.POST['observaciones']
		pedido.estado_pedido = EstadoPedido.objects.get(descripcion__contains='Rechazado')
		pedido.save()	
	return HttpResponseRedirect(reverse('gestion_pedidos'))

@login_required
def despachar_pedido(request,id_pedido):
	pedido = Pedido.objects.get(id=id_pedido)
	pedido.estado_pedido = EstadoPedido.objects.get(descripcion__contains='Enviado')
	pedido.save()
	return HttpResponseRedirect(reverse('gestion_pedidos'))

@login_required
def mis_facturas(request):
	categorias = Categoria.objects.all()
	facturas = Factura.objects.filter(cliente = UserProfile.objects.get(user=request.user))
	values={
		'categorias':categorias,
		'facturas':facturas,

	}
	return render_to_response('extranet/mis_facturas.html',values,context_instance=RequestContext(request))

@login_required
def registrar_pago(request,id_pedido):
	pedido = Pedido.objects.get(id=id_pedido)
	factura = pedido.factura_pedido
	factura.fecha_pago = date.today()
	factura.pagado = True
	factura.save()
	pedido.estado_pedido = EstadoPedido.objects.get(descripcion__contains="Finalizado")
	pedido.save()
	return HttpResponseRedirect(reverse('gestion_pedidos'))

@login_required
def ver_factura(request,id_factura):
	factura = Factura.objects.get(id = id_factura)
	detalle = factura.detalle.all()
	categorias = Categoria.objects.all()
	values={
		'factura':factura,
		'detalle':detalle,
		'categorias':categorias,
	}
	return render_to_response('extranet/factura.html',values,context_instance=RequestContext(request))


def ver_categoria(request,id_cat):
	categoria = Categoria.objects.get(id=id_cat)
	ofertas = Oferta.objects.all()
	of1 = ofertas.exclude(fecha_inicio__gte=datetime.now())
	ofertas = ofertas.exclude(fecha_fin__lte=datetime.now())
	for oferta in ofertas:
		producto = oferta.producto
		if not producto.categoria == categoria:
			ofertas = ofertas.exclude(id=oferta.id)
	
	productos = Producto.objects.all()
	for of in ofertas:
		p = of.producto.id
		productos = productos.exclude(id=p)
	for producto in productos:
		if not producto.categoria == categoria:
			productos = productos.exclude(id = producto.id)
	categorias = Categoria.objects.all()
	form = LoginForm()
	values={
		'form':form,
		'categorias':categorias,
		'ofertas':ofertas,
		'productos':productos,
	}
	return render_to_response('internet/cuerpo.html',values, context_instance = RequestContext(request))



def calcular_total_pedido(request):
	total=0
	pedido = request.session['pedido']
	productos_pedidos = ProductoPedido.objects.filter(pedido = pedido)
	for producto_pedido in productos_pedidos:
		if producto_pedido.cantidad:
			total = total +(producto_pedido.cantidad*producto_pedido.costo)
	return total

def is_pedido_valid(request):
	pedido = request.session['pedido']
	productos_pedidos = ProductoPedido.objects.filter(pedido=pedido)
	for producto_pedido in productos_pedidos:
		if not producto_pedido.cantidad:
			return False
	return True


