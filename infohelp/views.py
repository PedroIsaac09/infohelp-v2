from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.http import HttpResponseForbidden
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Curso, Dificuldade, Categoria, Aula
from .forms import CursoForm, DificuldadeForm, CategoriaForm
from .forms import AulaForm
from django.db.models import Q


# Mixin customizado para professores — sem depender de django-braces.
class ProfessorRequiredMixin(UserPassesTestMixin):
    group_required = 'Professor'

    def test_func(self):
        user = self.request.user
        if not user or not user.is_authenticated:
            return False
        if user.is_superuser:
            return True
        return user.groups.filter(name=self.group_required).exists()

    def handle_no_permission(self):
        context = {
            'title': 'Acesso não permitido',
            'subtitle': 'Ops — você não tem permissão para acessar esta área.',
            'detail': 'Esta seção é exclusiva para professores. Se você acredita que isto é um erro, entre em contato com a administração.'
        }
        return render(self.request, 'acesso_nao_permitido.html', context, status=403)
    



    
def index(request):
    return render(request, "index.html")


@login_required
def inicio(request):
    from usuarios.models import SolicitacaoProfessor
    
    # Verificar se há notificação de aprovação/rejeição não vista
    notificacao = None
    solicitacao_respondida = SolicitacaoProfessor.objects.filter(
        usuario=request.user,
        notificacao_vista=False
    ).exclude(status='pendente').first()
    
    if solicitacao_respondida:
        notificacao = solicitacao_respondida
    
    return render(request, "inicio.html", {'notificacao': notificacao})


def testegerencia(request):
    return render(request, "gerencia/pagina_gerencia.html")


@login_required
def perfil(request):
    from usuarios.forms import UserProfileForm, UserPasswordChangeForm, PerfilFotoForm
    from usuarios.models import PerfilUsuario
    from django.contrib import messages
    
    # Garanta que o perfil existe
    perfil_usuario, created = PerfilUsuario.objects.get_or_create(usuario=request.user)
    
    profile_form = None
    password_form = None
    foto_form = None
    tab = request.GET.get('tab', 'perfil')
    
    if request.method == 'POST':
        if 'profile_submit' in request.POST:
            # Processa formulário de perfil (nome, email, telefone, localizacao) E foto se enviada
            profile_form = UserProfileForm(request.POST, instance=perfil_usuario)
            foto_form = PerfilFotoForm(request.POST, request.FILES, instance=perfil_usuario)
            
            if profile_form.is_valid() and foto_form.is_valid():
                profile_form.save()
                foto_form.save()
                messages.success(request, 'Perfil e foto atualizados com sucesso!')
                return redirect('perfil')
            else:
                password_form = UserPasswordChangeForm(request.user)
        elif 'password_submit' in request.POST:
            password_form = UserPasswordChangeForm(request.user, request.POST)
            if password_form.is_valid():
                user = password_form.save()
                # Atualiza a sessão para evitar logout
                from django.contrib.auth import update_session_auth_hash
                update_session_auth_hash(request, user)
                messages.success(request, 'Senha alterada com sucesso!')
                tab = 'seguranca'
            else:
                tab = 'seguranca'
            profile_form = UserProfileForm(instance=perfil_usuario)
            foto_form = PerfilFotoForm(instance=perfil_usuario)
    else:
        profile_form = UserProfileForm(instance=perfil_usuario)
        password_form = UserPasswordChangeForm(request.user)
        foto_form = PerfilFotoForm(instance=perfil_usuario)
    
    context = {
        'profile_form': profile_form,
        'password_form': password_form,
        'foto_form': foto_form,
        'perfil_usuario': perfil_usuario,
        'tab': tab,
    }
    return render(request, "perfil.html", context)





#Biblioteca
@login_required
def biblioteca(request):
    # List courses saved by the current user
    items = request.user.biblioteca.select_related('curso').order_by('-data_adicionado')
    return render(request, 'biblioteca.html', {'items': items})


@login_required
def adicionar_biblioteca(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    # create if not exists
    from .models import Biblioteca
    obj, created = Biblioteca.objects.get_or_create(usuario=request.user, curso=curso)
    next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)


@login_required
def remover_biblioteca(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    from .models import Biblioteca
    Biblioteca.objects.filter(usuario=request.user, curso=curso).delete()
    next_url = request.POST.get('next') or request.GET.get('next') or request.META.get('HTTP_REFERER') or '/'
    return redirect(next_url)





# CRUD Cursos (Class-Based Views)

class CursoCreateView(ProfessorRequiredMixin, LoginRequiredMixin, CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'gerencia/criar_curso.html'
    success_url = reverse_lazy('listar_cursos')
    group_required = u'Professor'

    def form_valid(self, form):
        
        form.instance.usuario = self.request.user

        url = super().form_valid(form)

        return url


class CursoListView(ListView):
    model = Curso
    template_name = 'cursos.html'
    context_object_name = 'cursos'

    def get_queryset(self):
        q = self.request.GET.get('q', '').strip()
        qs = Curso.objects.all()
        if q:
            qs = qs.filter(
                Q(titulo__icontains=q) |
                Q(descricao__icontains=q) |
                Q(aulas__titulo__icontains=q) |
                Q(aulas__conteudo__icontains=q)
            ).distinct()
        return qs.order_by('-data_criacao')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        q = self.request.GET.get('q', '').strip()
        saved_course_ids = []
        if self.request.user.is_authenticated:
            saved_course_ids = list(self.request.user.biblioteca.values_list('curso_id', flat=True))
        context.update({'saved_course_ids': saved_course_ids, 'q': q})
        return context


class CursoUpdateView(ProfessorRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'gerencia/editar_curso.html'
    success_url = reverse_lazy('listar_cursos')
    group_required = u'Professor'

    def get_object(self, queryset=None):
        self.object = get_object_or_404(Curso, pk=self.kwargs.get('pk'), usuario=self.request.user)
        return self.object

class CursoDeleteView(ProfessorRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Curso
    template_name = 'gerencia/deletar_curso.html'
    success_url = reverse_lazy('listar_cursos')
    group_required = u'Professor'

    def get_object(self, queryset=None):
        self.object = get_object_or_404(Curso, pk=self.kwargs.get('pk'), usuario=self.request.user)
        return self.object



# CRUD Aulas (Class-Based Views)


class AulaCreateView(ProfessorRequiredMixin, LoginRequiredMixin, CreateView):
    model = Aula
    form_class = AulaForm
    template_name = 'aulas/criar_aula.html'
    group_required = u'Professor'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_superuser:
            self.curso = get_object_or_404(Curso, pk=kwargs.get('curso_id'))
        else:
            self.curso = get_object_or_404(Curso, pk=kwargs.get('curso_id'), usuario=request.user)
            
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.curso = self.curso

        form.instance.usuario = self.request.user

        return super().form_valid(form)

    def get_success_url(self):
        return reverse_lazy('listar_aulas', kwargs={'curso_id': self.curso.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso'] = self.curso
        return context


class AulaListView(ListView):
    model = Aula
    template_name = 'aulas/listar_aulas.html'
    context_object_name = 'aulas'

    def get_queryset(self):
        self.curso = get_object_or_404(Curso, pk=self.kwargs.get('curso_id'))
        return self.curso.aulas.all().order_by('ordem')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso'] = self.curso
        return context


# detalhe_aula permanece como função para lógica de embed de vídeo
@login_required
def detalhe_aula(request, curso_id, aula_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    aula = get_object_or_404(Aula, pk=aula_id, curso=curso)

    # Preparar URL embed para YouTube (ou retornar a URL direta para outros provedores)
    video_embed = None
    if aula.video:
        from urllib.parse import urlparse, parse_qs
        parsed = urlparse(aula.video)
        hostname = parsed.hostname or ''
        # YouTube watch URL: convert to embed
        if 'youtube' in hostname or 'youtu.be' in hostname:
            # handle youtu.be short links
            if 'youtu.be' in hostname:
                video_id = parsed.path.lstrip('/')
            else:
                qs = parse_qs(parsed.query)
                video_id = qs.get('v', [None])[0]
                if not video_id:
                    # fallback: path may contain /embed/{id}
                    parts = parsed.path.split('/')
                    video_id = parts[-1] if parts else None
            if video_id:
                video_embed = f'https://www.youtube.com/embed/{video_id}'
        else:
            # assume direct embeddable URL (e.g., mp4) or provider-compatible
            video_embed = aula.video

    return render(request, 'aulas/detalhe_aula.html', {'curso': curso, 'aula': aula, 'video_embed': video_embed})


class AulaUpdateView(ProfessorRequiredMixin, LoginRequiredMixin, UpdateView):
    model = Aula
    form_class = AulaForm
    template_name = 'aulas/editar_aula.html'
    pk_url_kwarg = 'aula_id'
    context_object_name = 'aula'
    group_required = u'Professor'

    def get_object(self, queryset=None):
        curso_id = self.kwargs.get('curso_id')
        
        if self.request.user.is_superuser:
            curso = get_object_or_404(Curso, pk=curso_id)
        else:
            curso = get_object_or_404(Curso, pk=curso_id, usuario=self.request.user)

        return get_object_or_404(Aula, pk=self.kwargs.get('aula_id'), curso=curso)

    def get_success_url(self):
        return reverse_lazy('listar_aulas', kwargs={'curso_id': self.kwargs.get('curso_id')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso'] = get_object_or_404(Curso, pk=self.kwargs.get('curso_id'))
        return context


class AulaDeleteView(ProfessorRequiredMixin, LoginRequiredMixin, DeleteView):
    model = Aula
    template_name = 'aulas/deletar_aula.html'
    pk_url_kwarg = 'aula_id'
    context_object_name = 'aula'
    group_required = u'Professor'

    def get_object(self, queryset=None):
        curso_id = self.kwargs.get('curso_id')
        
        if self.request.user.is_superuser:
            curso = get_object_or_404(Curso, pk=curso_id)
        else:
            curso = get_object_or_404(Curso, pk=curso_id, usuario=self.request.user)

        return get_object_or_404(Aula, pk=self.kwargs.get('aula_id'), curso=curso)

    def get_success_url(self):
        return reverse_lazy('listar_aulas', kwargs={'curso_id': self.kwargs.get('curso_id')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso'] = get_object_or_404(Curso, pk=self.kwargs.get('curso_id'))
        return context


class CursoCadastradosListView(ProfessorRequiredMixin, LoginRequiredMixin, ListView):
    model = Curso
    template_name = 'cursos_cadastrados.html'
    context_object_name = 'object_list'
    group_required = u'Professor'

    def get_queryset(self):
        return Curso.objects.filter(usuario=self.request.user).order_by('-data_criacao')