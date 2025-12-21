from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import (
    CustomLoginView, 
    register,
    solicitar_professor,
    listar_solicitacoes,
    aprovar_solicitacao,
    rejeitar_solicitacao,
    marcar_notificacao_vista
)

urlpatterns = [
    path("login/", CustomLoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("register/", register, name="register"),
    path("solicitar-professor/", solicitar_professor, name="solicitar_professor"),
    path("solicitacoes/", listar_solicitacoes, name="listar_solicitacoes"),
    path("solicitacoes/<int:solicitacao_id>/aprovar/", aprovar_solicitacao, name="aprovar_solicitacao"),
    path("solicitacoes/<int:solicitacao_id>/rejeitar/", rejeitar_solicitacao, name="rejeitar_solicitacao"),
    path("notificacao/<int:solicitacao_id>/vista/", marcar_notificacao_vista, name="marcar_notificacao_vista"),
]
