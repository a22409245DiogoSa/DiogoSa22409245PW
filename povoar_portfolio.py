import os
import django
import json

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from portfolio.models import Licenciatura, UnidadeCurricular

def povoar():
    print("\n--- Iniciando Povoamento Total ---")

    # 1. Garantir Licenciatura
    lic, _ = Licenciatura.objects.get_or_create(
        nome="Engenharia Informática",
        defaults={'apresentacao': "Licenciatura da Universidade Lusófona."}
    )

    # 2. Localizar JSON
    base_dir = os.path.dirname(os.path.abspath(__file__))
    caminho = os.path.join(base_dir, 'files', 'ULHT260-PT.json')

    if not os.path.exists(caminho):
        print(f"❌ Erro fatal: O ficheiro não existe em {caminho}")
        return

    with open(caminho, 'r', encoding='utf-8') as f:
        dados = json.load(f)
        ucs = dados.get('courseFlatPlan', [])
        
        print(f"Encontradas {len(ucs)} cadeiras no JSON.")

        for item in ucs:
            uc, created = UnidadeCurricular.objects.update_or_create(
                nome=item['curricularUnitName'],
                licenciatura=lic,
                defaults={
                    'ano': item['curricularYear'],
                    'ects': item['ects'],
                    'docente': "Docente a designar"
                }
            )
            prefixo = "✔ Inserida" if created else "↻ Atualizada"
            print(f"{prefixo}: {uc.nome} ({uc.ano}º ano)")

    print("\n--- Povoamento terminado com sucesso! ---")

if __name__ == "__main__":
    povoar()