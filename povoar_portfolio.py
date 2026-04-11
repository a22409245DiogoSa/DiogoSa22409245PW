import os
import django
import json

# 1. Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from portfolio.models import Licenciatura, UnidadeCurricular, Projeto

def povoar():
    print("--- A iniciar povoamento ---")

    # 2. Garante que a Licenciatura existe
    curso, created = Licenciatura.objects.get_or_create(
        nome="Engenharia Informática",
        defaults={'apresentacao': "Curso da Universidade Lusófona."}
    )
    if created: print("Licenciatura criada.")

    # 3. Carregar UCs (Pasta files)
    caminho_ucs = os.path.join('files', 'ULHT260-PT.json')
    if os.path.exists(caminho_ucs):
        with open(caminho_ucs, 'r', encoding='utf-8') as f:
            dados = json.load(f)
            for uc_json in dados.get('courseFlatPlan', []):
                uc, created = UnidadeCurricular.objects.get_or_create(
                    nome=uc_json['curricularUnitName'],
                    licenciatura=curso,
                    defaults={
                        'ano': uc_json['curricularYear'],
                        'ects': uc_json['ects'],
                        'docente': "Docente Lusófona"
                    }
                )
                if created: print(f"Inserida UC: {uc.nome}")
    else:
        print("Aviso: Ficheiro de UCs não encontrado.")

    # 4. Carregar TFCs (Pasta data)
    caminho_tfc = os.path.join('data', 'tfcs.json')
    if os.path.exists(caminho_tfc):
        with open(caminho_tfc, 'r', encoding='utf-8') as f:
            lista_tfcs = json.load(f)
            
            # Precisamos de uma UC para ligar o projeto (ex: Programação Web)
            uc_projeto = UnidadeCurricular.objects.filter(nome="Programação Web").first()
            
            if not uc_projeto:
                # Se PW ainda não existir, usamos a primeira que encontrar
                uc_projeto = UnidadeCurricular.objects.first()

            for item in lista_tfcs:
                projeto, created = Projeto.objects.get_or_create(
                    titulo=item.get('titulo'),
                    defaults={
                        'descricao': item.get('resumo', 'Sem descrição'),
                        'uc': uc_projeto,
                        'github': 'https://github.com/diogosa'
                    }
                )
                if created: print(f"Inserido TFC: {projeto.titulo}")
    else:
        print("Erro: Pasta 'data' ou ficheiro 'tfcs.json' não encontrado!")

    print("--- Povoamento concluído! ---")

if __name__ == "__main__":
    povoar()