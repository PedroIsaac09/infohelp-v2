from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import CreateView, ListView, UpdateView, DeleteView
from django.urls import reverse_lazy
from .models import Curso, Dificuldade, Categoria, Aula
from .forms import CursoForm, DificuldadeForm, CategoriaForm
from .forms import AulaForm
from django.db.models import Q






def criar_categoria(request):
    if request.method == 'POST':    
        form = CategoriaForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('criar_curso')
    else:
        form = CategoriaForm()
    return render(request, 'criar_categoria.html', {'form': form})

def editar_categoria(request, pk):
    categoria = Categoria.objects.get(pk=pk)
    if request.method == 'POST':
        form = CategoriaForm(request.POST, instance=categoria)
        if form.is_valid():
            form.save()
            return redirect('listar_categorias')
    else:
        form = CategoriaForm(instance=categoria)
    return render(request, 'editar_categoria.html', {'form': form})

def deletar_categoria(request, pk):
    categoria = Categoria.objects.get(pk=pk)
    if request.method == 'POST':
        categoria.delete()
        return redirect('listar_categorias')
    return render(request, 'deletar_categoria.html', {'categoria': categoria})





def criar_dificuldade(request):
    if request.method == 'POST':
        form = DificuldadeForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('criar_aula')  # ou a página que desejar
    else:
        form = DificuldadeForm()
    return render(request, 'criar_dificuldade.html', {'form': form})

def editar_dificuldade(request, pk):
    dificuldade = get_object_or_404(Dificuldade, pk=pk)
    if request.method == 'POST':
        form = DificuldadeForm(request.POST, instance=dificuldade)
        if form.is_valid():
            form.save()
            return redirect('listar_cursos')
    else:
        form = DificuldadeForm(instance=dificuldade)
    return render(request, 'editar_dificuldade.html', {'form': form})

def deletar_dificuldade(request, pk):
    dificuldade = get_object_or_404(Dificuldade, pk=pk)
    if request.method == 'POST':
        dificuldade.delete()
        return redirect('listar_cursos')
    return render(request, 'deletar_dificuldade.html', {'dificuldade': dificuldade})





def index(request):
    return render(request, "index.html")


@login_required
def inicio(request):
    return render(request, "inicio.html")


def testegerencia(request):
    return render(request, "gerencia/pagina_gerencia.html")


def perfil(request):
    return render(request, "perfil.html")





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

class CursoCreateView(LoginRequiredMixin, CreateView):
    model = Curso
    form_class = CursoForm
    template_name = 'gerencia/criar_curso.html'
    success_url = reverse_lazy('listar_cursos')

    def form_valid(self, form):
        # If you want to associate the curso to the logged user, uncomment:
        # curso = form.save(commit=False)
        # curso.usuario = self.request.user
        # curso.save()
        return super().form_valid(form)


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


class CursoUpdateView(LoginRequiredMixin, UpdateView):
    model = Curso
    form_class = CursoForm
    template_name = 'gerencia/editar_curso.html'
    success_url = reverse_lazy('listar_cursos')


class CursoDeleteView(LoginRequiredMixin, DeleteView):
    model = Curso
    template_name = 'gerencia/deletar_curso.html'
    success_url = reverse_lazy('listar_cursos')




# CRUD Aulas (Class-Based Views)


class AulaCreateView(LoginRequiredMixin, CreateView):
    model = Aula
    form_class = AulaForm
    template_name = 'aulas/criar_aula.html'

    def dispatch(self, request, *args, **kwargs):
        self.curso = get_object_or_404(Curso, pk=kwargs.get('curso_id'))
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.curso = self.curso
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


class AulaUpdateView(LoginRequiredMixin, UpdateView):
    model = Aula
    form_class = AulaForm
    template_name = 'aulas/editar_aula.html'
    pk_url_kwarg = 'aula_id'
    context_object_name = 'aula'

    def get_object(self, queryset=None):
        curso = get_object_or_404(Curso, pk=self.kwargs.get('curso_id'))
        return get_object_or_404(Aula, pk=self.kwargs.get('aula_id'), curso=curso)

    def get_success_url(self):
        return reverse_lazy('listar_aulas', kwargs={'curso_id': self.kwargs.get('curso_id')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso'] = get_object_or_404(Curso, pk=self.kwargs.get('curso_id'))
        return context


class AulaDeleteView(LoginRequiredMixin, DeleteView):
    model = Aula
    template_name = 'aulas/deletar_aula.html'
    pk_url_kwarg = 'aula_id'
    context_object_name = 'aula'

    def get_object(self, queryset=None):
        curso = get_object_or_404(Curso, pk=self.kwargs.get('curso_id'))
        return get_object_or_404(Aula, pk=self.kwargs.get('aula_id'), curso=curso)

    def get_success_url(self):
        return reverse_lazy('listar_aulas', kwargs={'curso_id': self.kwargs.get('curso_id')})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['curso'] = get_object_or_404(Curso, pk=self.kwargs.get('curso_id'))
        return context