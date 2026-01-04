from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView
from django.http import JsonResponse
from .models import Curso

class CursoListView(ListView):
    model = Curso
    template_name = 'cursos/lista_cursos.html'
    context_object_name = 'cursos'
    
    def get_queryset(self):
        # Optimizamos la carga de relaciones para evitar el error N+1
        return Curso.objects.all().select_related('instructor').prefetch_related('respaldos')

def curso_detail_api(request, slug):
    """
    Vista que devuelve toda la información del curso en JSON 
    para ser mostrada en el modal dinámico.
    """
    curso = get_object_or_404(
        Curso.objects.prefetch_related('modulos__lecciones', 'respaldos').select_related('instructor'), 
        slug=slug
    )
    
    # Estructuramos los datos para el frontend
    data = {
        'titulo': curso.titulo,
        'subtitulo': curso.subtitulo,
        'descripcion': curso.descripcion,
        'precio': str(curso.precio_principal),
        'certificacion_extra': str(curso.precio_certificacion_adicional),
        'instructor': {
            'nombre': curso.instructor.nombre,
            'titulo': curso.instructor.titulo_corto,
            'foto': curso.instructor.foto.url,
            'bio': curso.instructor.biografia
        },
        'detalles': {
            'horas': curso.horas_certificacion,
            'duracion_vivo': curso.duracion_en_vivo,
            'nivel': curso.get_nivel_display(),
            'fecha': curso.fecha_inicio.strftime('%d %b %Y'),
            'horario': curso.horario_clase.strftime('%H:%M p.m.')
        },
        'respaldos': [{'nombre': r.nombre, 'logo': r.logo_blanco.url} for r in curso.respaldos.all()],
        'temario': [
            {
                'titulo': m.titulo,
                'fecha': m.fecha_clase.strftime('%d/%m/%y') if m.fecha_clase else '',
                'lecciones': [l.titulo for l in m.lecciones.all()]
            } for m in curso.modulos.all()
        ]
    }
    return JsonResponse(data)