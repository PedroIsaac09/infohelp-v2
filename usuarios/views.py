from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate
from django.contrib.auth.views import LoginView
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import Group
from django.contrib import messages
from django.urls import reverse_lazy
from django.utils import timezone
from .forms import RegisterForm, LoginForm
from .models import SolicitacaoProfessor


class CustomLoginView(LoginView):
    template_name = "login.html"
    authentication_form = LoginForm


def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("inicio")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def home(request):
    return render(request, "infohelp/templates/inicio.html")


@login_required
def solicitar_professor(request):
    """View para usuário comum solicitar ser professor"""
    # Verificar se já é professor ou admin
    if request.user.is_superuser or request.user.groups.filter(name='Professor').exists():
        messages.warning(request, 'Você já é professor!')
        return redirect('perfil')
    
    # Verificar se já tem solicitação pendente
    if SolicitacaoProfessor.objects.filter(usuario=request.user, status='pendente').exists():
        messages.warning(request, 'Você já tem uma solicitação pendente!')
        return redirect('perfil')
    
    if request.method == 'POST':
        mensagem = request.POST.get('mensagem', '').strip()
        links = request.POST.get('links', '').strip()
        curriculo = request.FILES.get('curriculo')
        
        if not mensagem:
            messages.error(request, 'Por favor, descreva o motivo da sua solicitação.')
        elif not curriculo:
            messages.error(request, 'Por favor, anexe seu currículo.')
        else:
            SolicitacaoProfessor.objects.create(
                usuario=request.user,
                mensagem=mensagem,
                links=links if links else None,
                curriculo=curriculo
            )
            messages.success(request, 'Solicitação enviada com sucesso! Aguarde a análise de um administrador.')
            return redirect('perfil')
    
    return render(request, 'solicitar_professor.html')


def is_admin(user):
    """Verifica se o usuário é admin"""
    return user.is_superuser


@login_required
@user_passes_test(is_admin)
def listar_solicitacoes(request):
    """View para admin listar todas as solicitações"""
    solicitacoes = SolicitacaoProfessor.objects.select_related('usuario', 'admin_responsavel').all()
    
    context = {
        'solicitacoes': solicitacoes,
        'pendentes': solicitacoes.filter(status='pendente').count(),
    }
    return render(request, 'listar_solicitacoes.html', context)


@login_required
@user_passes_test(is_admin)
def aprovar_solicitacao(request, solicitacao_id):
    """View para admin aprovar solicitação"""
    solicitacao = get_object_or_404(SolicitacaoProfessor, id=solicitacao_id)
    
    if solicitacao.status != 'pendente':
        messages.warning(request, 'Esta solicitação já foi processada!')
        return redirect('listar_solicitacoes')
    
    if request.method == 'POST':
        mensagem_admin = request.POST.get('mensagem_admin', '')
        
        # Atualizar solicitação
        solicitacao.status = 'aprovada'
        solicitacao.mensagem_admin = mensagem_admin
        solicitacao.admin_responsavel = request.user
        solicitacao.data_resposta = timezone.now()
        solicitacao.save()
        
        # Adicionar usuário ao grupo Professor
        grupo_professor, created = Group.objects.get_or_create(name='Professor')
        solicitacao.usuario.groups.add(grupo_professor)
        
        messages.success(request, f'{solicitacao.usuario.username} agora é professor!')
        return redirect('listar_solicitacoes')
    
    return render(request, 'processar_solicitacao.html', {'solicitacao': solicitacao, 'acao': 'aprovar'})


@login_required
@user_passes_test(is_admin)
def rejeitar_solicitacao(request, solicitacao_id):
    """View para admin rejeitar solicitação"""
    solicitacao = get_object_or_404(SolicitacaoProfessor, id=solicitacao_id)
    
    if solicitacao.status != 'pendente':
        messages.warning(request, 'Esta solicitação já foi processada!')
        return redirect('listar_solicitacoes')
    
    if request.method == 'POST':
        mensagem_admin = request.POST.get('mensagem_admin', '')
        
        # Atualizar solicitação
        solicitacao.status = 'rejeitada'
        solicitacao.mensagem_admin = mensagem_admin
        solicitacao.admin_responsavel = request.user
        solicitacao.data_resposta = timezone.now()
        solicitacao.save()
        
        messages.success(request, f'Solicitação de {solicitacao.usuario.username} foi rejeitada.')
        return redirect('listar_solicitacoes')
    
    return render(request, 'processar_solicitacao.html', {'solicitacao': solicitacao, 'acao': 'rejeitar'})


@login_required
def marcar_notificacao_vista(request, solicitacao_id):
    """Marca a notificação de resposta como vista"""
    solicitacao = get_object_or_404(SolicitacaoProfessor, id=solicitacao_id, usuario=request.user)
    solicitacao.notificacao_vista = True
    solicitacao.save()
    return redirect('inicio')



