from django.shortcuts import render
from cursos.models import Curso

def home(request):
    cursos = Curso.objects.all().select_related('instructor')
    return render(request, 'index.html', {'cursos': cursos})

