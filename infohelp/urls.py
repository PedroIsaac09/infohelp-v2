from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('inicio/', views.inicio, name="inicio"),

    path('categorias/nova/', views.criar_categoria, name='criar_categoria'),
    path('categorias/<int:pk>/editar/', views.editar_categoria, name='editar_categoria'),
    path('categorias/<int:pk>/deletar/', views.deletar_categoria, name='deletar_categoria'),

    path('dificuldades/nova/', views.criar_dificuldade, name='criar_dificuldade'),
    path('dificuldades/<int:pk>/editar/', views.editar_dificuldade, name='editar_dificuldade'),
    path('dificuldades/<int:pk>/deletar/', views.deletar_dificuldade, name='deletar_dificuldade'),

    path('cursos/novo/', views.criar_curso, name='criar_curso'),
    path('cursos/', views.listar_cursos, name='listar_cursos'),
    path('cursos/<int:pk>/editar/', views.editar_curso, name='editar_curso'),
    path('cursos/<int:pk>/deletar/', views.deletar_curso, name='deletar_curso'),
    
    path('cursos/<int:curso_id>/aulas/', views.listar_aulas, name='listar_aulas'),
    path('cursos/<int:curso_id>/aulas/<int:aula_id>/', views.detalhe_aula, name='detalhe_aula'),
    path('cursos/<int:curso_id>/aulas/nova/', views.criar_aula, name='criar_aula'),
    path('cursos/<int:curso_id>/aulas/<int:aula_id>/editar/', views.editar_aula, name='editar_aula'),
    path('cursos/<int:curso_id>/aulas/<int:aula_id>/deletar/', views.deletar_aula, name='deletar_aula'),
    
    path('biblioteca/', views.biblioteca, name="biblioteca"),
    path('biblioteca/adicionar/<int:curso_id>/', views.adicionar_biblioteca, name='adicionar_biblioteca'),
    path('biblioteca/remover/<int:curso_id>/', views.remover_biblioteca, name='remover_biblioteca'),

    path('perfil/', views.perfil, name="perfil"),
    #Teste das páginas de gerenciamento
    path('testegerencia/', views.testegerencia, name="testegerencia"),
]