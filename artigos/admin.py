from django.contrib import admin

# Register your models here.
from .models import Artigo, Comentario
from django.contrib.auth.models import Group

# Criar o grupo programaticamente se não existir
#group, created = Group.objects.get_or_create(name='autores')
#
@admin.register(Artigo)
class ArtigoAdmin(admin.ModelAdmin):
    # Campos que aparecem na lista
    list_display = ('titulo', 'autor', 'data_criacao')
    
    # Esconde estes campos do formulário de edição/criação para não teres de preencher à mão
    exclude = ('autor', 'likes')

    def save_model(self, request, obj, form, change):
        if not change: # Se for um artigo novo, define o autor como o user logado
            obj.autor = request.user
        super().save_model(request, obj, form, change)