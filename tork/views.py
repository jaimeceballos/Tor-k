from django.shortcuts import render_to_response
from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponseRedirect, HttpResponse, Http404
import datetime
from django.conf import settings
from django.template import RequestContext
from apps.main.models import *
from apps.main.forms import LoginForm, UserProfileForm,RegistracionForm
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse

from django.views.decorators.cache import cache_control

@cache_control(must_revalidate=True, max_age=3600, private=True)
def pagina_inicio(request):
	
	categorias = Categoria.objects.all()
	form = LoginForm()
	ofertas = Oferta.objects.filter()

	
	values={
		
		'form':form,
		'categorias':categorias,
	}
	return render_to_response('internet/cuerpo.html',values, context_instance = RequestContext(request))

def login(request):
	if request.method == 'POST':
		form = LoginForm(request.POST)
		if form.is_valid():
			username = form.data['usuario']
			password  =  form.data['password']
			user = auth.authenticate(username=username, password=password)
			if user is not None and user.is_active:
				# Password valido, el usuario esta marcado como activo
				auth.login(request, user)
				return HttpResponseRedirect(reverse('inicio'))

@cache_control(must_revalidate=True, max_age=3600, private=True)
def logout(request):
    auth.logout(request)
    url = "/"
    return HttpResponseRedirect(url)

def registro(request):
	categorias = Categoria.objects.all()
	form = LoginForm()
	formr = RegistracionForm()
	if request.method == 'POST':
		formr = RegistracionForm(request.POST)
		if formr.is_valid():
			formr.save()
			user = User.objects.get(username=formr.cleaned_data['email'])
			profile = UserProfile.objects.get(user=user)
			print formr.cleaned_data['tipo_documento']
			profile.tipo_doc = formr.cleaned_data['tipo_documento']
			profile.nro_doc = formr.cleaned_data['numero_documento']
			profile.localidad = formr.cleaned_data['localidad']
			profile.calle = formr.cleaned_data['calle']
			profile.save()
			return HttpResponseRedirect("/")
	values={
		'form':form,
		'profile':formr,
		'categorias':categorias,
	}
	return render_to_response('internet/registro.html',values, context_instance = RequestContext(request))