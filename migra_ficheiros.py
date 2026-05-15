import os
import django
from django.core.files.base import ContentFile

# 1. Configurar o ambiente Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from portfolio.models import Projeto, MakingOf
from escola.models import Curso
from artigos.models import Artigo

def migrar_objeto(obj, campo_nome):
    """
    Versão corrigida para Cloudinary: 
    Lê o ficheiro local e guarda-o usando ContentFile para evitar erro de caminhos absolutos.
    """
    try:
        campo_ficheiro = getattr(obj, campo_nome)
        
        # Verifica se o campo tem um nome (referência na DB)
        if not campo_ficheiro or not campo_ficheiro.name:
            return False, "Campo vazio na base de dados"

        # Tenta encontrar o ficheiro no disco (na pasta media/)
        # Se estivermos no ambiente onde a pasta media existe:
        caminho_local = os.path.join('media', campo_ficheiro.name)
        
        if os.path.exists(caminho_local):
            print(f"   -> A enviar para Cloudinary: {campo_ficheiro.name}...")
            with open(caminho_local, 'rb') as f:
                # Usamos ContentFile para evitar o erro de 'absolute paths'
                conteudo = f.read()
                nome_ficheiro = os.path.basename(campo_ficheiro.name)
                campo_ficheiro.save(nome_ficheiro, ContentFile(conteudo), save=True)
            return True, "Sucesso"
        else:
            return False, f"Ficheiro não encontrado em: {caminho_local}"
            
    except Exception as e:
        return False, str(e)

def executar_migracao_total():
    modelos = [
        (Projeto, 'imagem', 'Projetos'),
        (MakingOf, 'foto_caderno', 'Making Of'),
        (Curso, 'imagem', 'Cursos'),
        (Artigo, 'fotografia', 'Artigos')
    ]

    for modelo, campo, nome_pt in modelos:
        print(f"\n--- Migrando {nome_pt} ---")
        objetos = modelo.objects.all()
        if not objetos:
            print(f"   ℹ️ Nenhum objeto encontrado para {nome_pt}.")
            continue
            
        for obj in objetos:
            sucesso, msg = migrar_objeto(obj, campo)
            if sucesso:
                print(f"   ✅ {obj} migrado.")
            else:
                print(f"   ⚠️ {obj}: {msg}")

if __name__ == "__main__":
    try:
        print("🚀 A iniciar migração (Fix: ContentFile)...")
        executar_migracao_total()
        print("\n✨ PROCESSO CONCLUÍDO!")
    except Exception as e:
        print(f"\n❌ Erro crítico: {e}")