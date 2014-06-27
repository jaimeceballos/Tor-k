#! /usr/bin/python
# -*- encoding: utf-8 -*-

from django import forms 
from apps.main.models import *


attrs_dict = { 'class': 'required' }

class LoginForm(forms.Form):
	usuario = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict)))
	password = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False))



class RegistracionForm(forms.Form):
    
    email = forms.EmailField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)), label=(u'Dirección de email'))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),label=(u'Clave'))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs=attrs_dict, render_value=False),label=(u'Clave (de nuevo)'))
    nombre	  = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)), label=(u'Nombre'))
    apellido  = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=75)), label=(u'Apellido'))	
    tipo_documento = forms.ModelChoiceField(widget=forms.Select(attrs=dict(attrs_dict)), queryset= TipoDoc.objects.all(),label=(u'Tipo de documento'))
    numero_documento = forms.IntegerField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=10)), label=(u'Numero Documento'))
    localidad        = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=100)), label=(u'Ciudad')) 
    calle        = forms.CharField(widget=forms.TextInput(attrs=dict(attrs_dict, maxlength=100)), label=(u'Calle')) 

    def clean_username(self):
        
        """
        Valida si el username ya existe en la base de datos
        """
        try:
            user = User.objects.get(username__iexact=self.cleaned_data['email'])
        except User.DoesNotExist:
            return self.cleaned_data['email']
        raise forms.ValidationError(_(u'Este email ya esta registrado en nuestra base de datos.'))
    
    
    def clean(self):
        """
        Verificamos si password1 y password2 son iguales
        """
        if 'password1' in self.cleaned_data and 'password2' in self.cleaned_data:
            if self.cleaned_data['password1'] != self.cleaned_data['password2']:
                raise forms.ValidationError((u'Tienes que ingresar la misma clave en los dos campos'))
        return self.cleaned_data
    
        
    def save(self, profile_callback=None):
        """
        Creamos el usuario, el cliente y relacionamos el cliente con el usuario
        """
        
        username = self.cleaned_data['email']
        password = self.cleaned_data['password1']
        email    = self.cleaned_data['email']
        
        usuario = User.objects.create_user(username, email, password)
        usuario.is_active = True
        usuario.first_name = self.cleaned_data['nombre']
        usuario.last_name = self.cleaned_data['apellido']
        usuario.save()
        
        return usuario

class UserProfileForm(forms.ModelForm):

	class Meta:
		model = UserProfile
		exclude = ('user',)

class CategoriaForm(forms.ModelForm):

    class Meta:
        model = Categoria

class ProductoForm(forms.ModelForm):

    class Meta:
        model=Producto

class OfertaForm(forms.ModelForm):
    categoria = forms.ModelChoiceField(widget=forms.Select(), queryset= Categoria.objects.all(),label=(u'Categoria'))
    fecha_inicio = forms.DateField(widget=forms.DateInput())
    class Meta:
        model = Oferta