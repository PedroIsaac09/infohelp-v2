from django.shortcuts import render, redirect, get_object_or_404
from .models import Curso, Dificuldade,Categoria
from .forms import CursoForm, DificuldadeForm,CategoriaForm

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
            return redirect('criar_curso')  # ou a página que desejar
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
    return render(request, 'criar_curso.html', {'form': form})

def listar_cursos(request):
    cursos = Curso.objects.all().order_by('-data_criacao')
    return render(request, 'cursos.html', {'cursos': cursos})

def editar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES, instance=curso)
        if form.is_valid():
            form.save()
            return redirect('listar_cursos')
    else:
        form = CursoForm(instance=curso)
    return render(request, 'editar_curso.html', {'form': form, 'curso': curso})

def deletar_curso(request, pk):
    curso = get_object_or_404(Curso, pk=pk)
    if request.method == 'POST':
        curso.delete()
        return redirect('listar_cursos')
    return render(request, 'deletar_curso.html', {'curso': curso})




def biblioteca(request):
    return render(request, "biblioteca.html")

def login(request):
    return render(request, "login.html")

def cadastro(request):
    return render(request, "cadastro.html")


def testecursos(request):
    if request.method == 'POST':
        form = CursoForm(request.POST, request.FILES)
        if form.is_valid():
            curso = form.save(commit=False)
            curso.save()
            return redirect('listar_cursos')
    else:
        form = CursoForm()
    return render(request, "gerencia/cadastrar_curso.html", {'form': form})

def testegerencia(request):
    return render(request, "gerencia/pagina_gerencia.html")