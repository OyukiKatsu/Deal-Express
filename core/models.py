from django.db import models

# Create your models here.
from django.db import models
from django.core.exceptions import ValidationError
import re
from django.contrib.auth.models import User

# Clase Empresa
class Empresa(models.Model):
    nombre = models.CharField(max_length=50, verbose_name='Nombre', db_column='nombre')
    direccion = models.CharField(max_length=255, verbose_name='Direccion', db_column='direccion')
    pais = models.CharField(max_length=255, verbose_name='Pais', db_column='pais')

    class Meta:
        db_table= 'Empresa'
        verbose_name ='Empresa'
        verbose_name_plural ='Empresas'

    def __str__(self):
        return self.nombre



# Clase Usuario
class Profile(User):
    dni = models.CharField(max_length=9, unique=True, verbose_name='DNI', db_column='dni')
    correo = models.EmailField(unique=True, verbose_name='Correo Electronico', db_column='correo')
    imagen_perfil = models.ImageField(upload_to='usuarios/', verbose_name='Imagen de Perfil', db_column='imagen_perfil', blank=True, null=True, default='core/perfil_predeterminado.jpg')
    is_empresa = models.BooleanField(default=False, verbose_name='Quiere registrarse como empresa?', db_column='is_empresa')
    empresa_id = models.ForeignKey(to=Empresa, null=True, verbose_name='Empresa', db_column='empresa_id', on_delete=models.SET_NULL, default=None, related_name='get_Empresa_Usuarios', blank=True)


    class Meta:
        db_table= 'Profile'
        verbose_name ='Perfil'
        verbose_name_plural ='Perfiles'

    def clean(self):
        super().clean()

        
        if not re.match(r'^[0-9]{8}[A-Za-z]$', self.dni):
            raise ValidationError("El DNI debe tener 8 dígitos seguidos de una letra.")
        
       
        numeros = int(self.dni[:8])
        letra = self.dni[-1].upper()
        letras_dni = "TRWAGMYFPDXBNJZSQVHLCKE"
        letra_correcta = letras_dni[numeros % 23]

        if letra != letra_correcta:
            raise ValidationError(f"El DNI es incorrecto")
        
    def __str__(self):
        return super().username
    
#Clase Categoria
class Categoria(models.Model):
    nombre = models.CharField(max_length=30, primary_key=True, verbose_name='Nombre', db_column='nombre')
    
    class Meta:
        db_table= 'Categoria'
        verbose_name ='Categoria'
        verbose_name_plural ='Categorias'

#Clase SubCategoria
class SubCategoria(models.Model):
    nombre = models.CharField(max_length=30, verbose_name='Nombre', db_column='nombre')
    categoria_id = models.ForeignKey(to=Categoria, on_delete=models.CASCADE, verbose_name="Categoria", db_column="categoria", related_name='get_Categoria_SubCategoria')
    
    class Meta:
        db_table= 'SubCategoria'
        verbose_name ='SubCategoria'
        verbose_name_plural ='SubCategorias'

# Clase Producto
class Producto(models.Model):
    id = models.CharField(max_length=50, primary_key=True, verbose_name='ID', db_column='id')
    nombre = models.CharField(max_length=100, verbose_name='Nombre', db_column='nombre')
    imagen = models.ImageField(upload_to='productos/', verbose_name='Imagen de Producto', db_column='imagen')
    descripcion = models.TextField(verbose_name='Descripcion', db_column='descripcion')
    empresa_id = models.ForeignKey(to=Empresa, on_delete=models.CASCADE, verbose_name='Empresa', db_column='empresa_id', related_name='get_Empresa_Productos')
    subCategoria_id = models.ForeignKey(to=SubCategoria, on_delete=models.CASCADE, verbose_name='SubCategoria', db_column='subCategoria_id', related_name='get_SubCategoria_Productos')

    class Meta:
        db_table= 'Producto'
        verbose_name ='Producto'
        verbose_name_plural ='Productos'

    def __str__(self):
        return self.nombre

# Clase Oferta
class Producto_Listing(models.Model):
    precio = models.DecimalField(max_digits=10, decimal_places=2, verbose_name='Precio', db_column='precio')
    stock = models.PositiveIntegerField(verbose_name='Stock', db_column='stock')
    producto_id = models.ForeignKey(to=Producto, verbose_name='Producto', db_column='producto_id', on_delete=models.CASCADE, related_name='get_Producto_Ofertas')
    empresa_id = models.ForeignKey(to=Empresa, verbose_name='Empresa', db_column='empresa_id', on_delete=models.CASCADE, related_name='get_Empresa_Listing')
    
    class Meta:
        db_table= 'Producto_Listing'
        verbose_name ='Oferta'
        verbose_name_plural ='Ofertas'

    def __str__(self):
        return f"{self.producto_id.nombre} ofrecido por {self.empresa_id.nombre} a {self.precio} €"
    



class Carrito_Detalle(models.Model):
    unidades = models.PositiveIntegerField(verbose_name='Unidades', db_column='unidades')
    estado_venta = models.BooleanField(default=False, verbose_name='Estado', db_column='estado_venta')
    user_id = models.ForeignKey(to=Profile, on_delete=models.CASCADE, verbose_name='Usuario', db_column='user_id' , related_name='get_Usuario_Carritos')
    producto_listing_id = models.ForeignKey(to=Producto_Listing, verbose_name='Oferta', db_column='producto_listing_id', on_delete=models.CASCADE, related_name='get_ProductoListing_CarritoDetalles')
    

    class Meta:
        db_table= 'Carrito_Detalle'
        verbose_name ='Detalle Carrito'
        verbose_name_plural ='Detalle Carrito'


class Venta(models.Model):
    fecha = models.DateTimeField()
    user_id = models.ForeignKey(to=Profile, on_delete=models.CASCADE, verbose_name='Usuario', db_column='user_id' , related_name='get_Usuario_Factura')
    carrito_detalle_id = models.ManyToManyField(to=Carrito_Detalle, verbose_name='Detalle Carrito', db_column='carrito_detalle_id', related_name='get_Usuario_Factura')

    class Meta:
        db_table= 'Factura'
        verbose_name ='Factura'
        verbose_name_plural ='Facturas'   