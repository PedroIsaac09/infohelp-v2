from usuarios.models import PerfilUsuario, SolicitacaoProfessor


def perfil_usuario(request):
    """
    Adiciona o perfil do usuário autenticado ao contexto de todos os templates.
    """
    if request.user.is_authenticated:
        try:
            perfil = PerfilUsuario.objects.get(usuario=request.user)
        except PerfilUsuario.DoesNotExist:
            perfil = None
        return {'perfil_usuario': perfil}
    return {'perfil_usuario': None}


def solicitacoes_pendentes(request):
    """
    Adiciona o número de solicitações de professor pendentes ao contexto.
    Visível apenas para administradores.
    """
    if request.user.is_superuser:
        count = SolicitacaoProfessor.objects.filter(status='pendente').count()
        return {'solicitacoes_pendentes_count': count}
    return {'solicitacoes_pendentes_count': 0}
