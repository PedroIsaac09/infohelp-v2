import os
import sys
import django

# Configurar o Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

# Executar makemigrations
from django.core.management import call_command

print("=" * 60)
print("CRIANDO MIGRATIONS PARA SISTEMA DE SOLICITAÇÃO DE PROFESSOR")
print("=" * 60)
print("\nCriando migrations...")
call_command('makemigrations', 'usuarios', verbosity=2)
print("\n" + "=" * 60)
print("APLICANDO MIGRATIONS")
print("=" * 60)
call_command('migrate', verbosity=2)
print("\n" + "=" * 60)
print("✓ CONCLUÍDO COM SUCESSO!")
print("=" * 60)
print("\nNovos campos adicionados:")
print("  • curriculo - Upload de arquivo (PDF, DOC, DOCX)")
print("  • links - Links opcionais para LinkedIn, GitHub, etc.")
print("\nAgora os usuários podem anexar currículo e adicionar links!")
print("=" * 60)
