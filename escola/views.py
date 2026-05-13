# Create your views here.
##  ficheiro escola/views.py

from django.shortcuts import render
from .models import Curso

def cursos_view(request):
    cursos = (
        Curso.objects
        .select_related('professor')
        .prefetch_related('alunos')
        .all()
    )
    return render(request, 'cursos_online.html', {'cursos': cursos})
