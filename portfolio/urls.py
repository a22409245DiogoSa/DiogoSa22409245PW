from django.urls import path
from . import views

app_name = 'portfolio'

urlpatterns = [
    # Se quiser que a página do portfolio apareça em /portfolio/
    path('', views.home_page_view, name='home'), 
    path('projetos/', views.projetos_list_view, name='projetos_list'),
    path('projetos/novo/', views.novo_projeto_view, name='novo_projeto'),
    path('projetos/edita/<int:id>/', views.edita_projeto_view, name='edita_projeto'),
    path('projetos/apaga/<int:id>/', views.apaga_projeto_view, name='apaga_projeto'),
    path('licenciatura/nova/', views.nova_licenciatura_view, name='nova_licenciatura'),
    path('licenciatura/edita/<int:id>/', views.edita_licenciatura_view, name='edita_licenciatura'),
    path('uc/nova/', views.nova_uc_view, name='nova_uc'),
    path('uc/edita/<int:id>/', views.edita_uc_view, name='edita_uc'),
    path('tecnologia/nova/', views.nova_tecnologia_view, name='nova_tecnologia'),
    path('tecnologia/edita/<int:id>/', views.edita_tecnologia_view, name='edita_tecnologia'),
    path('tecnologia/apaga/<int:id>/', views.apaga_tecnologia_view, name='apaga_tecnologia'),
    path('importar-ei/', views.importar_ei_lusofona, name='importar_ei'),
]