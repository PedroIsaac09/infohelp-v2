from django.contrib import admin
from .models import PerfilUsuario


@admin.register(PerfilUsuario)
class PerfilUsuarioAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'telefone', 'localizacao', 'data_criacao')
    search_fields = ('usuario__username', 'usuario__email', 'telefone', 'localizacao')
    readonly_fields = ('data_criacao', 'data_atualizacao')
    fieldsets = (
        ('Usuário', {
            'fields': ('usuario', 'foto')
        }),
        ('Informações de Contato', {
            'fields': ('telefone', 'localizacao')
        }),
        ('Biografia', {
            'fields': ('bio',)
        }),
        ('Datas', {
            'fields': ('data_criacao', 'data_atualizacao'),
            'classes': ('collapse',)
        }),
    )
