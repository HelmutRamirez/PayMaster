from django.db import models

# Create your models here.
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
    imagen=models.ImageField(upload_to='photos')

    def __str__(self):
        return self.primer_nombre
