from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("admin/", admin.site.urls),
    path("escola/", include("escola.urls")), 
    path('accounts/', include('accounts.urls')),
    path('artigos/', include('artigos.urls')), 
    path('', include('portfolio.urls')),
]

# Isto permite que o Django sirva as fotos do caderno e dos projetos
