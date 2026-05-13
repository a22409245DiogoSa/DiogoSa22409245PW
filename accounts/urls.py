from django.urls import path
from . import views

# Este é o namespace que o erro dizia que faltava
app_name = 'accounts' 

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registo/', views.registo_view, name='registo'),
    path('magic-request/', views.solicitar_link_magico, name='magic_request'),
    path('magic-login/<str:token>/', views.validar_link_magico, name='magic_login'),
]