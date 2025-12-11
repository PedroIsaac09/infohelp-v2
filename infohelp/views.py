from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Curso, Dificuldade, Categoria, Aula
from .forms import CursoForm, DificuldadeForm, CategoriaForm
from .forms import AulaForm 

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


def inicio(request):
    return render(request, "inicio.html")




def criar_curso(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save(commit=False)
            #curso.usuario = request.user  # Associa o curso ao usuário logado
            curso.save()
            return redirect('listar_cursos')
    else:
        form = CursoForm()
    return render(request, "gerencia/criar_curso.html", {'form': form})

from django.db.models import Q


def listar_cursos(request):
    q = request.GET.get('q', '').strip()
    cursos = Curso.objects.all()
    if q:
        # filter by course title, course description, aula title or aula content
        cursos = cursos.filter(
            Q(titulo__icontains=q) |
            Q(descricao__icontains=q) |
            Q(aulas__titulo__icontains=q) |
            Q(aulas__conteudo__icontains=q)
        ).distinct()
    cursos = cursos.order_by('-data_criacao')

    saved_course_ids = []
    if request.user.is_authenticated:
        saved_course_ids = list(request.user.biblioteca.values_list('curso_id', flat=True))
    return render(request, 'cursos.html', {'cursos': cursos, 'saved_course_ids': saved_course_ids, 'q': q})

def editar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('listar_cursos')
    else:
        form = CursoForm(instance=curso)
    return render(request, 'gerencia/editar_curso.html', {'form': form, 'curso': curso})

def deletar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        curso.delete()
        return redirect('listar_cursos')
    return render(request, 'gerencia/deletar_curso.html', {'curso': curso})




def criar_aula(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    if request.method == 'POST':
        form = AulaForm(request.POST, request.FILES)
        if form.is_valid():
            aula = form.save(commit=False)
            aula.curso = curso
            aula.save()
            return redirect('listar_aulas', curso_id=curso_id)
    else:
        form = AulaForm()
    return render(request, 'aulas/criar_aula.html', {'form': form, 'curso': curso})


def listar_aulas(request, curso_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    aulas = curso.aulas.all().order_by('ordem')
    return render(request, 'aulas/listar_aulas.html', {'curso': curso, 'aulas': aulas})


@login_required
def inicio(request):
    return render(request, "inicio.html")


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


def editar_aula(request, curso_id, aula_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    aula = get_object_or_404(Aula, pk=aula_id, curso=curso)
    if request.method == 'POST':
        form = AulaForm(request.POST, request.FILES, instance=aula)
        if form.is_valid():
            form.save()
            return redirect('listar_aulas', curso_id=curso_id)
    else:
        form = AulaForm(instance=aula)
    return render(request, 'aulas/editar_aula.html', {'form': form, 'curso': curso, 'aula': aula})


def deletar_aula(request, curso_id, aula_id):
    curso = get_object_or_404(Curso, pk=curso_id)
    aula = get_object_or_404(Aula, pk=aula_id, curso=curso)
    if request.method == 'POST':
        aula.delete()
        return redirect('listar_aulas', curso_id=curso_id)
    return render(request, 'aulas/deletar_aula.html', {'curso': curso, 'aula': aula})


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

def testegerencia(request):
    return render(request, "gerencia/pagina_gerencia.html")


def perfil(request):
    return render(request, "perfil.html")