from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('inicio/', views.inicio, name="inicio"),

    path('cursos/novo/', views.CursoCreateView.as_view(), name='criar_curso'),
    path('cursos/', views.CursoListView.as_view(), name='listar_cursos'),
    path('cursos/cadastrados/', views.CursoCadastradosListView.as_view(), name='cursos_cadastrados'),
    path('cursos/<int:pk>/editar/', views.CursoUpdateView.as_view(), name='editar_curso'),
    path('cursos/<int:pk>/deletar/', views.CursoDeleteView.as_view(), name='deletar_curso'),
    
    path('cursos/<int:curso_id>/aulas/', views.AulaListView.as_view(), name='listar_aulas'),
    path('cursos/<int:curso_id>/aulas/<int:aula_id>/', views.detalhe_aula, name='detalhe_aula'),
    path('cursos/<int:curso_id>/aulas/nova/', views.AulaCreateView.as_view(), name='criar_aula'),
    path('cursos/<int:curso_id>/aulas/<int:aula_id>/editar/', views.AulaUpdateView.as_view(), name='editar_aula'),
    path('cursos/<int:curso_id>/aulas/<int:aula_id>/deletar/', views.AulaDeleteView.as_view(), name='deletar_aula'),
    
    path('biblioteca/', views.biblioteca, name="biblioteca"),
    path('biblioteca/adicionar/<int:curso_id>/', views.adicionar_biblioteca, name='adicionar_biblioteca'),
    path('biblioteca/remover/<int:curso_id>/', views.remover_biblioteca, name='remover_biblioteca'),

    path('perfil/', views.perfil, name="perfil"),
    #Teste das páginas de gerenciamento
    path('testegerencia/', views.testegerencia, name="testegerencia"),
]