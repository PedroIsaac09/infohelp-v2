from django.contrib import admin
from django.utils.html import format_html
from .models import PerfilUsuario, SolicitacaoProfessor


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


@admin.register(SolicitacaoProfessor)
class SolicitacaoProfessorAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'status', 'tem_curriculo', 'ver_curriculo', 'tem_links', 'data_solicitacao', 'admin_responsavel')
    list_filter = ('status', 'data_solicitacao')
    search_fields = ('usuario__username', 'usuario__email', 'mensagem')
    readonly_fields = ('data_solicitacao', 'visualizar_curriculo', 'visualizar_links')
    fieldsets = (
        ('Solicitante', {
            'fields': ('usuario', 'mensagem')
        }),
        ('Documentação', {
            'fields': ('curriculo', 'visualizar_curriculo', 'links', 'visualizar_links')
        }),
        ('Status', {
            'fields': ('status', 'mensagem_admin', 'admin_responsavel', 'data_resposta')
        }),
        ('Datas', {
            'fields': ('data_solicitacao',)
        }),
    )
    
    def tem_curriculo(self, obj):
        return '✓' if obj.curriculo else '✗'
    tem_curriculo.short_description = 'Currículo'
    
    def ver_curriculo(self, obj):
        if obj.curriculo:
            return format_html(
                '<a href="{}" target="_blank" class="button" style="background-color: #417690; color: white; padding: 5px 10px; text-decoration: none; border-radius: 4px;">📄 Baixar</a>',
                obj.curriculo.url
            )
        return '-'
    ver_curriculo.short_description = 'Download'
    
    def visualizar_curriculo(self, obj):
        if obj.curriculo:
            return format_html(
                '<a href="{}" target="_blank" style="display: inline-block; background-color: #417690; color: white; padding: 10px 20px; text-decoration: none; border-radius: 5px; font-weight: bold;">📄 Baixar Currículo</a><br><small style="color: #666;">Arquivo: {}</small>',
                obj.curriculo.url,
                obj.curriculo.name.split('/')[-1]
            )
        return format_html('<span style="color: #999;">Nenhum currículo anexado</span>')
    visualizar_curriculo.short_description = 'Currículo Anexado'
    
    def visualizar_links(self, obj):
        if obj.links:
            links_list = obj.links.strip().split('\n')
            html_links = '<div style="line-height: 1.8;">'
            for link in links_list:
                link = link.strip()
                if link:
                    url = link if link.startswith('http') else f'https://{link}'
                    html_links += f'<a href="{url}" target="_blank" style="color: #417690; text-decoration: none;">🔗 {link}</a><br>'
            html_links += '</div>'
            return format_html(html_links)
        return format_html('<span style="color: #999;">Nenhum link informado</span>')
    visualizar_links.short_description = 'Links Relevantes'
    
    def tem_links(self, obj):
        return '✓' if obj.links else '✗'
    tem_links.short_description = 'Links'
