from django.db import models

# Create your models here.
## ficheiro models.py

class Professor(models.Model):
    nome = models.CharField(max_length=100)
    email = models.EmailField()

    def __str__(self):
        return self.nome

class Aluno(models.Model):
    nome = models.CharField(max_length=100)
    numero = models.CharField(max_length=20, unique=True)
    fotografia = models.ImageField(upload_to='fotos_alunos/')

    def __str__(self):
        return self.nome

class Curso(models.Model):
    nome = models.CharField(max_length=100)
    professor = models.ForeignKey(Professor, on_delete=models.CASCADE, related_name='cursos')
    alunos = models.ManyToManyField(Aluno, related_name='cursos')

    def __str__(self):
        return self.nome