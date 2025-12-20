from django import template

register = template.Library()

@register.filter
def in_group(user, group_name):
    """Retorna True se o usuário pertence ao grupo `group_name` ou for superuser."""
    try:
        if not user or not getattr(user, 'is_authenticated', False):
            return False
        if user.is_superuser:
            return True
        return user.groups.filter(name=group_name).exists()
    except Exception:
        return False
