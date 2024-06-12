from django.db import models  # type: ignore
from django.core.validators import MaxValueValidator  # type: ignore


class Empresa(models.Model):
    nit = models.CharField(max_length=50, primary_key=True)
    razon_social = models.CharField(max_length=100) 
    telefono_entidad = models.CharField(max_length=15) 
    correo_entidad = models.EmailField() 
    imagen=models.ImageField(upload_to='photos')

    def __str__(self):
        return self.razon_social


class Empleado(models.Model):
    estado_civil=[
        ('SOLTERO', 'Soltero/a'),
        ('CASADO', 'Casado/a'),
        ('DIVORCIADO', 'Divorciado/a'),
        ('VIUDO', 'Viudo/a'),
    ]
    tipo_documento=[
        ('Cc', 'Cedula de ciudadania'),
        ('Ce', 'Cedula de extrangeria'),
        ('Passpor', 'Pasaporte'),
    ]
    genero=[
        ('M', 'Masculino'),
        ('F', 'Femenino'),
        ('O', 'Otro'),
        ('P', 'Prefiero no decir'),
    ]

    numero_identificacion = models.IntegerField(primary_key=True, max_length=10)
    primer_nombre = models.CharField(max_length=30)
    segundo_nombre = models.CharField(max_length=30, blank=True, null=True)
    primer_apellido = models.CharField(max_length=30)
    segundo_apellido = models.CharField(max_length=30, blank=True, null=True)
    estado_civil = models.CharField(max_length=20, choices=estado_civil)
    tipo_documento = models.CharField(max_length=50, choices=tipo_documento)
    correo = models.EmailField(unique=True)
    celular = models.CharField(max_length=15)
    genero = models.CharField(max_length=10,choices=genero)
    fecha_nacimiento = models.DateField()
    fecha_exp_documento = models.DateField()
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE) 
    imagen=models.ImageField(upload_to='photos')

    def __str__(self):
        return self.primer_nombre



class Usuarios(models.Model):
    id_rol=[
        ('Contador', 'Contador'),
        ('Auxiliar Contable', 'Auxiliar Contable'),
        ('RRHH', 'RRHH'),
        ('Empleado General', 'Empleado General'),
    ]

    usuario = models.ForeignKey(Empleado, on_delete=models.CASCADE) 
    intentos = models.IntegerField(default=0)
    estado_u = models.BooleanField(default=True)
    contrasena = models.CharField(max_length=128, null=True)
    id_rol= models.CharField(max_length=30,choices=id_rol) 
    
  



