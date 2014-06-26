from django.db import models
from django.contrib.auth.models import User
from django.db.models import signals
# Create your models here.

class TipoDoc(models.Model):
	descripcion 	= models.CharField(max_length=10,unique=True)

	def __unicode__(self):
		return u"%s" % self.descripcion
	
	class Meta:
		db_table = 'tipo_documento'


class UserProfile(models.Model):
	user 		= models.OneToOneField(User)
	tipo_doc	= models.ForeignKey('TipoDoc',null=True,blank=True)
	nro_doc		= models.IntegerField(null=True,blank=True)
	localidad	= models.CharField(max_length=100,null=True,blank=True)
	calle		= models.CharField(max_length=100,null=True,blank=True)
	apto		= models.BooleanField(default=True)
	anulado		= models.BooleanField(default=False)

	class Meta:
		db_table = 'UserProfile'
		unique_together= ('tipo_doc','nro_doc',)

	def user_profile(sender, instance, signal,*args,**kwargs):
		profile, new = UserProfile.objects.get_or_create(user=instance)

	signals.post_save.connect(user_profile,sender=User)

class Provincia(models.Model):
	nombre		= models.CharField(max_length=50)

	class Meta:
		db_table	= 'provincia'

class Localidad(models.Model):
	nombre		= models.CharField(max_length=50)
	provincia 	= models.ForeignKey('Provincia')

	class Meta:
		db_table='localidad'	

class EstadoPedido(models.Model):
	descripcion	= models.CharField(max_length=50)

	class Meta:
		db_table = 'estado_pedido'

class Categoria(models.Model):
	descripcion	= models.CharField(max_length=100)

	def __unicode__(self):
		return u"%s" % self.descripcion

	def puedo_eliminar():
		"""este metodo se encarga de verificar si se puede eliminar el tuit"""

		return User.objects.get(username=request.user).is_staff()

	class Meta:
		db_table = 'categoria'

class Producto(models.Model):
	categoria 		= models.ForeignKey('Categoria')
	descripcion		= models.CharField(max_length=100)
	stock_minimo	= models.IntegerField()
	punto_reorden	= models.IntegerField()
	stock_maximo	= models.IntegerField()
	stock_actual	= models.IntegerField()
	imagen			= models.ImageField(upload_to='productos/', null=True, blank=True)
	costo			= models.DecimalField(max_digits=7, decimal_places=2)

	class Meta:
		db_table	= 'producto'


class Pedido(models.Model):
	fecha_carga		= models.DateField(auto_now=True)
	cliente 		= models.ForeignKey('UserProfile')
	estado_pedido	= models.ForeignKey('EstadoPedido')

	class Meta:
		db_table	= 'pedido'

class ProductoPedido(models.Model):
	pedido 		= models.ForeignKey('Pedido')
	producto 	= models.ForeignKey('Producto')
	cantidad	= models.IntegerField()
	anulado		= models.BooleanField(default=False)
	costo		= models.DecimalField(max_digits=5, decimal_places=2)

	class Meta:
		db_table	= 'producto_pedido'

class TipoFactura(models.Model):
	descripcion 	= models.CharField(max_length=100)

	class Meta:
		db_table	= 'tipo_factura'



class Factura(models.Model):
	tipo 	= models.ForeignKey('TipoFactura')
	numero	= models.IntegerField()
	pedido 	= models.ForeignKey('Pedido')
	fecha 	= models.DateField()

	class Meta:
		db_table =	'factura'

class DetalleFactura(models.Model):
	factura 		= models.ForeignKey('Factura')
	pedido_producto	= models.ForeignKey('ProductoPedido')
	costo			= models.DecimalField(max_digits=5,decimal_places=2)

	class Meta:
		db_table 	= 'detalle_factura'

class Oferta(models.Model):
	producto 		= models.ForeignKey('Producto')
	fecha_inicio	= models.DateField()
	fecha_fin		= models.DateField()
	costo			= models.DecimalField(max_digits=5,decimal_places=2)

	class Meta:
		db_table = 'Oferta'

