from django.db import models
from django.contrib.auth.models import User


class PerfilUsuario(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, related_name='perfil')
    foto = models.ImageField(upload_to='perfis/', blank=True, null=True)
    bio = models.TextField(blank=True, null=True, max_length=500)
    telefone = models.CharField(max_length=20, blank=True, null=True)
    localizacao = models.CharField(max_length=255, blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    data_atualizacao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Perfil de {self.usuario.username}"
    
    class Meta:
        verbose_name = "Perfil do Usuário"
        verbose_name_plural = "Perfis de Usuários"


class SolicitacaoProfessor(models.Model):
    STATUS_CHOICES = [
        ('pendente', 'Pendente'),
        ('aprovada', 'Aprovada'),
        ('rejeitada', 'Rejeitada'),
    ]
    
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solicitacoes_professor')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pendente')
    mensagem = models.TextField(help_text='Por que você deseja se tornar professor?')
    curriculo = models.FileField(upload_to='curriculos/', help_text='Envie seu currículo (PDF, DOC, DOCX)')
    links = models.TextField(blank=True, null=True, help_text='Links para portfólio, LinkedIn, GitHub, etc. (opcional)')
    mensagem_admin = models.TextField(blank=True, null=True, help_text='Resposta do administrador')
    notificacao_vista = models.BooleanField(default=False, help_text='Se o usuário já viu a notificação de resposta')
    data_solicitacao = models.DateTimeField(auto_now_add=True)
    data_resposta = models.DateTimeField(blank=True, null=True)
    admin_responsavel = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='solicitacoes_respondidas')
    
    def __str__(self):
        return f"Solicitação de {self.usuario.username} - {self.get_status_display()}"
    
    class Meta:
        verbose_name = "Solicitação de Professor"
        verbose_name_plural = "Solicitações de Professor"
        ordering = ['-data_solicitacao']

