from django.contrib import admin
from django.utils.html import format_html
from .models import Instructor, InstitucionRespaldo, Curso, Modulo, Leccion

# --- INLINES PARA EDICIÓN RÁPIDA ---

class LeccionInline(admin.TabularInline):
    model = Leccion
    extra = 1
    fields = ('orden', 'titulo', 'duracion_minutos', 'es_gratis', 'video_url')
    sortable_field_name = "orden"

class ModuloInline(admin.StackedInline):
    model = Modulo
    extra = 1
    show_change_link = True
    classes = ('collapse',) # Permite contraer los módulos para no saturar la vista
    fields = (('orden', 'titulo'), 'fecha_clase')

# --- CONFIGURACIONES DE MODELOS ---

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    list_display = ('mostrar_foto', 'nombre', 'titulo_corto', 'linkedin')
    search_fields = ('nombre', 'titulo_corto')
    
    def mostrar_foto(self, obj):
        if obj.foto:
            return format_html('<img src="{}" style="width: 45px; height: 45px; border-radius: 50%; object-fit: cover;" />', obj.foto.url)
        return "Sin foto"
    mostrar_foto.short_description = 'Imagen'

@admin.register(InstitucionRespaldo)
class InstitucionRespaldoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'mostrar_logo')
    
    def mostrar_logo(self, obj):
        if obj.logo_blanco:
            return format_html('<div style="background:#001A3D; padding:5px; display:inline-block; border-radius:4px;"><img src="{}" style="height: 30px;"/></div>', obj.logo_blanco.url)
        return "Sin logo"

@admin.register(Curso)
class CursoAdmin(admin.ModelAdmin):
    # Organización de la lista principal
    list_display = ('mostrar_portada', 'titulo', 'instructor', 'nivel', 'precio_principal', 'en_vivo', 'fecha_inicio')
    list_filter = ('nivel', 'en_vivo', 'instructor', 'fecha_inicio')
    search_fields = ('titulo', 'subtitulo')
    list_editable = ('en_vivo', 'precio_principal')
    prepopulated_fields = {'slug': ('titulo',)}
    
    # Inlines para gestionar la estructura desde el Curso
    inlines = [ModuloInline]

    # Organización estética del formulario de edición
    fieldsets = (
        ('Información Principal', {
            'fields': (('titulo', 'slug'), 'subtitulo', 'descripcion', 'instructor', 'respaldos')
        }),
        ('Diseño y Multimedia', {
            'fields': ('portada', 'en_vivo'),
            'description': 'Configuración visual de la Card en el inicio'
        }),
        ('Estructura de Precios', {
            'fields': (('precio_principal', 'precio_certificacion_adicional'),),
            'classes': ('wide',)
        }),
        ('Metadata Técnica', {
            'fields': (
                ('horas_certificacion', 'duracion_en_vivo', 'nivel'),
                ('meses_grabaciones', 'grupo_whatsapp', 'materiales_descargables')
            ),
        }),
        ('Programación de Clases', {
            'fields': (('fecha_inicio', 'horario_clase'),),
        }),
    )

    def mostrar_portada(self, obj):
        if obj.portada:
            return format_html('<img src="{}" style="width: 80px; height: 45px; border-radius: 4px; object-fit: cover;" />', obj.portada.url)
        return "Sin imagen"
    mostrar_portada.short_description = 'Portada'

@admin.register(Modulo)
class ModuloAdmin(admin.ModelAdmin):
    list_display = ('orden', 'titulo', 'curso', 'fecha_clase')
    list_filter = ('curso',)
    inlines = [LeccionInline] # Permite añadir lecciones dentro del módulo

@admin.register(Leccion)
class LeccionAdmin(admin.ModelAdmin):
    list_display = ('orden', 'titulo', 'modulo', 'duracion_minutos', 'es_gratis')
    list_filter = ('modulo__curso', 'es_gratis')
    search_fields = ('titulo',)