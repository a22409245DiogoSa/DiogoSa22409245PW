from django.db import models

# Create your models here.
from django.contrib.auth.models import User

class Artigo(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    fotografia = models.ImageField(upload_to='artigos/', blank=True, null=True)
    link_externo = models.URLField(blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='artigos')
    likes = models.ManyToManyField(User, related_name='artigos_curtidos', blank=True)

    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.titulo

class Comentario(models.Model):
    artigo = models.ForeignKey(Artigo, on_delete=models.CASCADE, related_name='comentarios')
    autor = models.ForeignKey(User, on_delete=models.CASCADE)
    texto = models.TextField()
    data_criacao = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Comentário de {self.autor.username} em {self.artigo.titulo}'