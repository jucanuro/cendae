from django.db import models
from django.core.validators import MinValueValidator
from django.utils.text import slugify

class Instructor(models.Model):
    nombre = models.CharField(max_length=100)
    titulo_corto = models.CharField(max_length=100, help_text="Ej: Psicólogo / Arquitecto de Datos")
    biografia = models.TextField()
    foto = models.ImageField(upload_to='instructors/')
    linkedin = models.URLField(blank=True)

    def __str__(self):
        return self.nombre

class InstitucionRespaldo(models.Model):
    nombre = models.CharField(max_length=100)
    logo_blanco = models.FileField(upload_to='respaldos/', help_text="Logo en formato SVG o PNG blanco")

    def __str__(self):
        return self.nombre

class Curso(models.Model):
    NIVEL_CHOICES = [
        ('basico', 'Básico'),
        ('intermedio', 'Intermedio'),
        ('avanzado', 'Avanzado'),
    ]

    titulo = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True)
    subtitulo = models.CharField(max_length=300, help_text="Frase de impacto inicial")
    descripcion = models.TextField()
    en_vivo = models.BooleanField(default=False)
    
    portada = models.ImageField(upload_to='cursos/portadas/')
    precio_principal = models.DecimalField(max_digits=10, decimal_places=2)
    precio_certificacion_adicional = models.DecimalField(max_digits=10, decimal_places=2, default=25.00)
    
    horas_certificacion = models.IntegerField(default=20)
    duracion_en_vivo = models.IntegerField(help_text="Horas totales de clases en vivo")
    nivel = models.CharField(max_length=20, choices=NIVEL_CHOICES, default='basico')
    meses_grabaciones = models.IntegerField(default=12)
    grupo_whatsapp = models.BooleanField(default=True)
    materiales_descargables = models.BooleanField(default=True)

    instructor = models.ForeignKey(Instructor, on_delete=models.PROTECT, related_name='cursos')
    respaldos = models.ManyToManyField(InstitucionRespaldo, blank=True)

    fecha_inicio = models.DateField()
    horario_clase = models.TimeField()

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.titulo)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.titulo

class Modulo(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='modulos')
    titulo = models.CharField(max_length=200, help_text="Ej: Estadística Descriptiva")
    orden = models.PositiveIntegerField(default=1)
    fecha_clase = models.DateField(null=True, blank=True)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return f"{self.curso.titulo} - {self.titulo}"

class Leccion(models.Model):
    modulo = models.ForeignKey(Modulo, on_delete=models.CASCADE, related_name='lecciones')
    titulo = models.CharField(max_length=200)
    duracion_minutos = models.IntegerField(default=15)
    es_gratis = models.BooleanField(default=False, help_text="¿Es una lección de prueba?")
    orden = models.PositiveIntegerField(default=1)
    
    # Para el contenido (puedes usar un campo para video o texto)
    video_url = models.URLField(blank=True, null=True)

    class Meta:
        ordering = ['orden']

    def __str__(self):
        return self.titulo