from django.urls import path
from . import views

app_name = 'artigos'

urlpatterns = [
    path('', views.listagem_artigos, name='listagem'),
    path('<int:artigo_id>/', views.detalhe_artigo, name='detalhe'),
    path('<int:artigo_id>/comentar/', views.publicar_comentario, name='comentar'),
    path('<int:artigo_id>/like/', views.dar_like, name='like'),
]