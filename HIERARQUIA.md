# Sistema de Hierarquia e Solicitação de Professor

## Visão Geral
Sistema implementado para gerenciar a hierarquia de usuários no InfoHelp com solicitação de cargo de professor.

## Hierarquia de Usuários

### 1. Usuário Comum (Padrão)
- Pode visualizar cursos e aulas
- Pode adicionar cursos à biblioteca
- Pode solicitar ser professor

### 2. Professor (Grupo)
- Todas as permissões de usuário comum
- Pode criar e gerenciar cursos
- Pode criar e gerenciar aulas
- Acesso à página "Cursos Cadastrados"

### 3. Administrador (Superuser)
- Todas as permissões de professor
- Pode aprovar/rejeitar solicitações de professor
- Pode adicionar usuários ao grupo Professor manualmente
- Acesso ao painel admin do Django
- Acesso à página de "Solicitações"

## Fluxo de Solicitação

### Para Usuário Comum:
1. Acessar o perfil
2. Clicar em "Ser Professor" (botão destacado na sidebar)
3. Preencher o formulário:
   - **Mensagem**: Explicar o motivo (obrigatório)
   - **Currículo**: Anexar PDF, DOC ou DOCX (obrigatório)
   - **Links**: Adicionar LinkedIn, GitHub, portfólio, etc. (opcional)
4. Aguardar aprovação do administrador

### Para Administrador:
1. Acessar "Admin" na barra de navegação superior
2. Visualizar todas as solicitações (pendentes, aprovadas, rejeitadas)
3. Clicar em "Aprovar" ou "Rejeitar"
4. Opcionalmente adicionar mensagem de resposta
5. Confirmar a ação

## URLs Implementadas

```python
# Usuário comum
/solicitar-professor/          # Formulário de solicitação

# Administrador
/solicitacoes/                 # Lista todas solicitações
/solicitacoes/<id>/aprovar/    # Aprovar solicitação
/solicitacoes/<id>/rejeitar/   # Rejeitar solicitação
```

## Modelos

### SolicitacaoProfessor
```python
usuario             # ForeignKey para User (solicitante)
status              # pendente, aprovada, rejeitada
mensagem            # Justificativa do usuário (obrigatório)
curriculo           # FileField para upload de CV (opcional)
links               # TextField para links relevantes (opcional)
mensagem_admin      # Resposta do administrador (opcional)
data_solicitacao    # Auto-preenchido
data_resposta       # Preenchido ao aprovar/rejeitar
admin_responsavel   # ForeignKey para User (admin que respondeu)
```

## Regras de Negócio

1. **Solicitação Única**: Usuário só pode ter uma solicitação pendente por vez
2. **Bloqueio para Professores**: Professores e admins não podem solicitar
3. **Aprovação Automática**: Ao aprovar, usuário é adicionado ao grupo "Professor" automaticamente
4. **Histórico**: Todas solicitações são mantidas para auditoria
5. **Mensagens**: Administrador pode adicionar mensagem de resposta (opcional)
6. **Currículo**: Aceita PDF, DOC, DOCX até 5MB (obrigatório)
7. **Links**: Campo de texto livre para múltiplos links (opcional)
8. **Anexos Visíveis**: Admin pode visualizar e baixar currículo na análise

## Templates Criados

1. `solicitar_professor.html` - Formulário de solicitação
2. `listar_solicitacoes.html` - Lista para admin
3. `processar_solicitacao.html` - Aprovar/Rejeitar

## Próximos Passos (Opcional)

- [ ] Sistema de notificações para avisar usuário sobre resposta
- [ ] Dashboard de estatísticas de solicitações
- [ ] Filtros avançados na lista de solicitações
- [ ] Exportar relatórios de solicitações
- [ ] Permitir múltiplas tentativas com cooldown

## Comandos Importantes

```bash
# Criar migrations
python manage.py makemigrations usuarios

# Aplicar migrations
python manage.py migrate

# Criar superusuário (se não tiver)
python manage.py createsuperuser

# Criar grupo Professor manualmente
python manage.py shell
>>> from django.contrib.auth.models import Group
>>> Group.objects.get_or_create(name='Professor')
```

## Testes Recomendados

1. **Como Usuário Comum:**
   - Fazer login
   - Ir ao perfil
   - Clicar em "Ser Professor"
   - Enviar solicitação

2. **Como Admin:**
   - Fazer login como superuser
   - Clicar em "Admin" no menu
   - Visualizar solicitações
   - Aprovar uma solicitação
   - Verificar que o usuário virou professor

3. **Verificação:**
   - Fazer login como o usuário aprovado
   - Verificar que agora tem acesso a "Cursos Cadastrados"
   - Tentar criar um curso
