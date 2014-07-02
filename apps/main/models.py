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
	tipo_doc	= models.ForeignKey('TipoDoc',null=True,blank=True,on_delete=models.PROTECT)
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
	provincia 	= models.ForeignKey('Provincia',on_delete=models.PROTECT)

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

		return User.objects.get(username=request.user).is_staff()

	class Meta:
		db_table = 'categoria'

class Producto(models.Model):
	categoria 		= models.ForeignKey('Categoria',on_delete=models.PROTECT)
	nombre			= models.CharField(max_length=100)
	marca			= models.CharField(max_length=100)
	espec			= models.TextField(max_length=250,null=True,blank=True)
	stock_minimo	= models.IntegerField()
	punto_reorden	= models.IntegerField()
	stock_maximo	= models.IntegerField()
	stock_actual	= models.IntegerField()
	imagen			= models.ImageField(upload_to='productos/', null=True, blank=True)
	costo			= models.DecimalField(max_digits=7, decimal_places=2)

	def puedo_eliminar():

		return User.objects.get(username=request.user).is_staff()

	def __unicode__(self):
		return u"%s - %s" % (self.nombre,self.marca)

	class Meta:
		db_table	= 'producto'


class TipoEnvio(models.Model):
	descripcion 	= models.CharField(max_length=40)

	def __unicode__(self):
		return u'%s' % self.descripcion

	class Meta:
		db_table 	= 'tipo_envio'

class MetodoPago(models.Model):
	descripcion 	= models.CharField(max_length=40)

	def __unicode__(self):
		return u'%s' % self.descripcion

	class Meta:
		db_table 	= 'metodo_pago'

class Pedido(models.Model):
	fecha_carga		= models.DateField(auto_now=True)
	cliente 		= models.ForeignKey('UserProfile',on_delete=models.PROTECT)
	estado_pedido	= models.ForeignKey('EstadoPedido',on_delete=models.PROTECT)
	tipo_envio		= models.ForeignKey('TipoEnvio', on_delete=models.PROTECT,null=True,blank=True)
	metodo_pago		= models.ForeignKey('MetodoPago', on_delete=models.PROTECT,null=True,blank=True)
	observaciones	= models.CharField(max_length=100,blank=True,null=True)

	class Meta:
		db_table	= 'pedido'

class ProductoPedido(models.Model):
	pedido 		= models.ForeignKey('Pedido',on_delete=models.PROTECT)
	producto 	= models.ForeignKey('Producto',on_delete=models.PROTECT)
	cantidad	= models.IntegerField(null=True,blank=True)
	anulado		= models.BooleanField(default=False)
	costo		= models.DecimalField(max_digits=7, decimal_places=2,null=True,blank=True)
	observaciones	= models.CharField(max_length=100,blank=True,null=True)


	class Meta:
		db_table	= 'producto_pedido'

class TipoFactura(models.Model):
	descripcion 	= models.CharField(max_length=100)

	def __unicode__(self):
		return u'%s' % self.descripcion
	
	class Meta:
		db_table	= 'tipo_factura'



class Factura(models.Model):
	cliente	= models.ForeignKey('UserProfile',on_delete=models.PROTECT)
	tipo 	= models.ForeignKey('TipoFactura',on_delete=models.PROTECT,null=True,blank=True)
	pedido 	= models.ForeignKey('Pedido',on_delete=models.PROTECT)
	fecha 	= models.DateField(auto_now=True)
	total	= models.DecimalField(max_digits=10,decimal_places=2,null=True,blank=True)


	class Meta:
		db_table =	'factura'
		unique_together = ('cliente','pedido',)

class DetalleFactura(models.Model):
	factura 		= models.ForeignKey('Factura',on_delete=models.PROTECT)
	pedido_producto	= models.ForeignKey('ProductoPedido',on_delete=models.PROTECT)
	costo			= models.DecimalField(max_digits=10,decimal_places=2)

	class Meta:
		db_table 	= 'detalle_factura'

class Oferta(models.Model):
	producto 		= models.ForeignKey('Producto',on_delete=models.PROTECT)
	fecha_inicio	= models.DateField()
	fecha_fin		= models.DateField()
	costo			= models.DecimalField(max_digits=7,decimal_places=2)

	def puedo_eliminar():

		return User.objects.get(username=request.user).is_staff()

	class Meta:
		db_table = 'Oferta'

