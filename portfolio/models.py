from django.db import models

class Licenciatura(models.Model):
    nome = models.CharField(max_length=100)
    apresentacao = models.TextField()
    def __str__(self):
        return self.nome

class Tecnologia(models.Model):
    nome = models.CharField(max_length=50)
    logotipo = models.ImageField(upload_to='tecnologias/', blank=True)
    link_oficial = models.URLField()
    def __str__(self):
        return self.nome

class UnidadeCurricular(models.Model):
    nome = models.CharField(max_length=100)
    ano = models.IntegerField()
    ects = models.IntegerField()
    docente = models.CharField(max_length=100)
    licenciatura = models.ForeignKey(Licenciatura, on_delete=models.CASCADE)
    def __str__(self):
        return self.nome

class Projeto(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    imagem = models.ImageField(upload_to='projetos/')
    github = models.URLField()
    uc = models.ForeignKey(UnidadeCurricular, on_delete=models.CASCADE)
    tecnologias = models.ManyToManyField(Tecnologia)
    def __str__(self):
        return self.titulo

class MakingOf(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    foto_caderno = models.ImageField(upload_to='makingof/')
    def __str__(self):
        return self.titulo