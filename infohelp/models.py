from django.db import models
from django.contrib.auth.models import User

class Categoria(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome
    
class Dificuldade(models.Model):
    nome = models.CharField(max_length=100)
    descricao = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.nome

class Curso(models.Model):
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    categoria = models.ForeignKey(Categoria, on_delete=models.SET_NULL, null=True, related_name='cursos')
    dificuldade = models.ForeignKey(Dificuldade, on_delete=models.SET_NULL, null=True, related_name='cursos')
    #usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='cursos')  # Dono/professor
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)
    ativo = models.BooleanField(default=True)
    imagem = models.ImageField(upload_to='cursos/', blank=True, null=True)
    link_video = models.URLField(blank=True, null=True)
    carga_horaria = models.PositiveIntegerField(help_text='Carga horária em horas', blank=True, null=True)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return self.titulo

class Aula(models.Model):
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='aulas')
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    video = models.URLField(blank=True, null=True)
    imagem = models.ImageField(upload_to='aulas/', blank=True, null=True)
    ordem = models.PositiveIntegerField(help_text='Ordem da aula no curso', default=1)
    usuario = models.ForeignKey(User, on_delete=models.PROTECT)

    def __str__(self):
        return f'{self.titulo} ({self.curso.titulo})'

class Biblioteca(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='biblioteca')
    curso = models.ForeignKey(Curso, on_delete=models.CASCADE, related_name='favoritos')
    data_adicionado = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.username} - {self.curso.titulo}"

