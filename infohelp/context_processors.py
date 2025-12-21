from usuarios.models import PerfilUsuario


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
