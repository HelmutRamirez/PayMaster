from django.db import models
from django.core.validators import MaxValueValidator


class Empresa(models.Model):
    nit = models.CharField(max_length=50, primary_key=True)
    telefono_entidad = models.CharField(max_length=15) 
    razon_social = models.CharField(max_length=100) 
    correo_entidad = models.EmailField() 


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

    numero_identificacion = models.CharField(validators=[MaxValueValidator(10)],primary_key=True)
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
    
    # intentos = models.IntegerField(default=0)
    # estado_u = models.BooleanField(default=True)
    # contrasena = models.CharField(max_length=128)
