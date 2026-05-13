from django.shortcuts import render, get_object_or_404, redirect
from .models import Artigo, Comentario
from django.contrib.auth.decorators import login_required

def listagem_artigos(request):
    artigos = Artigo.objects.all().order_by('-data_criacao')
    return render(request, 'artigos/listagem.html', {'artigos': artigos})

def detalhe_artigo(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)
    comentarios = artigo.comentarios.all().order_by('data_criacao')
    return render(request, 'artigos/detalhe.html', {
        'artigo': artigo,
        'comentarios': comentarios
    })

@login_required
def publicar_comentario(request, artigo_id):
    if request.method == 'POST':
        artigo = get_object_or_404(Artigo, id=artigo_id)
        texto = request.POST.get('texto')
        if texto:
            Comentario.objects.create(
                artigo=artigo,
                autor=request.user,
                texto=texto
            )
    return redirect('artigos:detalhe', artigo_id=artigo_id)

def dar_like(request, artigo_id):
    artigo = get_object_or_404(Artigo, id=artigo_id)
    if request.user.is_authenticated:
        if request.user in artigo.likes.all():
            artigo.likes.remove(request.user)
        else:
            artigo.likes.add(request.user)
    return redirect('artigos:listagem')