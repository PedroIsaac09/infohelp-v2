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
    
    path('biblioteca/', views.biblioteca, name="biblioteca"),

    #Teste das páginas de gerenciamento
    path('testegerencia/', views.testegerencia, name="testegerencia"),
]