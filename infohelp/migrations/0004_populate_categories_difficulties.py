from django.db import migrations


def create_categories_and_difficulties(apps, schema_editor):
    Categoria = apps.get_model('infohelp', 'Categoria')
    Dificuldade = apps.get_model('infohelp', 'Dificuldade')

    categorias = [
        'Desenvolvimento',
        'Programação',
        'Design e Multimídia',
        'Banco de Dados',
        'Inteligência Artificial',
        'Cloud Computing',
        'Segurança da Informação',
        'Infraestrutura e Redes',
        'Suporte e Manutenção',
        'Gestão e Produtividade em TI',
        'Eletrônica e Robótica',
        'Escritório e Ferramentas Digitais',
        'Redes Sociais e Marketing Digital',
    ]

    dificuldades = [
        'Iniciante',
        'Intermediário',
        'Avançado',
    ]

    for nome in categorias:
        Categoria.objects.get_or_create(nome=nome)

    for nome in dificuldades:
        Dificuldade.objects.get_or_create(nome=nome)


def remove_categories_and_difficulties(apps, schema_editor):
    Categoria = apps.get_model('infohelp', 'Categoria')
    Dificuldade = apps.get_model('infohelp', 'Dificuldade')

    categorias = [
        'Desenvolvimento',
        'Programação',
        'Design e Multimídia',
        'Banco de Dados',
        'Inteligência Artificial',
        'Cloud Computing',
        'Segurança da Informação',
        'Infraestrutura e Redes',
        'Suporte e Manutenção',
        'Gestão e Produtividade em TI',
        'Eletrônica e Robótica',
        'Escritório e Ferramentas Digitais',
        'Redes Sociais e Marketing Digital',
    ]

    dificuldades = [
        'Iniciante',
        'Intermediário',
        'Avançado',
    ]

    Categoria.objects.filter(nome__in=categorias).delete()
    Dificuldade.objects.filter(nome__in=dificuldades).delete()


class Migration(migrations.Migration):

    dependencies = [
        ('infohelp', '0003_remove_curso_usuario'),
    ]

    operations = [
        migrations.RunPython(create_categories_and_difficulties, remove_categories_and_difficulties),
    ]
