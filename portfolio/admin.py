from django.contrib import admin
from .models import Licenciatura, Tecnologia, UnidadeCurricular, Projeto, MakingOf

admin.site.register(Licenciatura)
admin.site.register(Tecnologia)
admin.site.register(UnidadeCurricular)
admin.site.register(Projeto)
admin.site.register(MakingOf)