from django.urls import path
from . import views

# Este é o namespace que o erro dizia que faltava
app_name = 'accounts' 

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('registo/', views.registo_view, name='registo'),
]