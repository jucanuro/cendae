# cursos/urls.py
from django.urls import path
from .views import CursoListView, curso_detail_api

app_name = 'cursos'

urlpatterns = [
    path('', CursoListView.as_view(), name='lista_cursos'), 
    path('api/curso/<slug:slug>/', curso_detail_api, name='curso_detail_api'),
]