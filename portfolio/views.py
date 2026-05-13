from django.shortcuts import render, redirect, get_object_or_404
from .models import Projeto, Tecnologia, UnidadeCurricular, Licenciatura
from .forms import ProjetoForm, TecnologiaForm, LicenciaturaForm, UnidadeCurricularForm
import requests
# Create your views here.

def home_page_view(request):
    context = {
        'projetos': Projeto.objects.all(),
        'tecnologias': Tecnologia.objects.all(),
        'unidades': UnidadeCurricular.objects.all(),
    }
    return render(request, 'portfolio/home.html', context)


def projetos_list_view(request):
    projetos = Projeto.objects.all()
    return render(request, 'portfolio/projetos_list.html', {'projetos': projetos})

def novo_projeto_view(request):
    form = ProjetoForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('portfolio:projetos_list')
    return render(request, 'portfolio/projeto_form.html', {'form': form, 'titulo': 'Novo Projeto'})

def edita_projeto_view(request, id):
    projeto = get_object_or_404(Projeto, id=id)
    form = ProjetoForm(request.POST or None, request.FILES or None, instance=projeto)
    if form.is_valid():
        form.save()
        return redirect('portfolio:projetos_list')
    return render(request, 'portfolio/projeto_form.html', {'form': form, 'titulo': 'Editar Projeto'})

def apaga_projeto_view(request, id):
    projeto = get_object_or_404(Projeto, id=id)
    if request.method == 'POST':
        projeto.delete()
        return redirect('portfolio:projetos_list')
    return render(request, 'portfolio/confirmar_apagar.html', {'item': projeto})


def nova_licenciatura_view(request):
    form = LicenciaturaForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('portfolio:home')
    return render(request, 'portfolio/projeto_form.html', {'form': form, 'titulo': 'Adicionar Licenciatura'})

def edita_licenciatura_view(request, id):
    licenciatura = get_object_or_404(Licenciatura, id=id)
    form = LicenciaturaForm(request.POST or None, instance=licenciatura)
    if form.is_valid():
        form.save()
        return redirect('portfolio:home')
    return render(request, 'portfolio/projeto_form.html', {'form': form, 'titulo': 'Editar Licenciatura'})


# --- VIEWS PARA TECNOLOGIA ---
def nova_tecnologia_view(request):
    form = TecnologiaForm(request.POST or None, request.FILES or None)
    if form.is_valid():
        form.save()
        return redirect('portfolio:home')
    return render(request, 'portfolio/projeto_form.html', {'form': form, 'titulo': 'Nova Tecnologia'})

def edita_tecnologia_view(request, id):
    objeto = get_object_or_404(Tecnologia, id=id)
    form = TecnologiaForm(request.POST or None, request.FILES or None, instance=objeto)
    if form.is_valid():
        form.save()
        return redirect('portfolio:home')
    return render(request, 'portfolio/projeto_form.html', {'form': form, 'titulo': 'Editar Tecnologia'})

def apaga_tecnologia_view(request, id):
    objeto = get_object_or_404(Tecnologia, id=id)
    if request.method == 'POST':
        objeto.delete()
        return redirect('portfolio:home')
    return render(request, 'portfolio/confirmar_apagar.html', {'item': objeto})

# --- VIEWS PARA UNIDADE CURRICULAR ---
def nova_uc_view(request):
    form = UnidadeCurricularForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('portfolio:home')
    return render(request, 'portfolio/projeto_form.html', {'form': form, 'titulo': 'Nova Unidade Curricular'})

def edita_uc_view(request, id):
    objeto = get_object_or_404(UnidadeCurricular, id=id)
    form = UnidadeCurricularForm(request.POST or None, instance=objeto)
    if form.is_valid():
        form.save()
        return redirect('portfolio:home')
    return render(request, 'portfolio/projeto_form.html', {'form': form, 'titulo': 'Editar Unidade Curricular'})


def importar_ei_lusofona(request):
    # ID do curso de Engenharia Informática (costuma ser 401 ou similar, verifica no URL do site)
    url = "https://www.ulusofona.pt/api/cursos/licenciatura/411"
    response = requests.get(url)
    dados = response.json()
    
    # ISTO VAI MOSTRAR TUDO NO TERMINAL DO VS CODE
    print("--- DADOS RECEBIDOS DA API ---")
    print(dados) 
    print("------------------------------")
    
    curso_id = 401 
    url = f"https://www.ulusofona.pt/api/cursos/licenciatura/{curso_id}"
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            dados = response.json()
            
            # Criar a Licenciatura se não existir
            licenciatura, _ = Licenciatura.objects.get_or_create(
                nome="Engenharia Informática",
                defaults={'apresentacao': 'Curso focado no desenvolvimento de software e sistemas.'}
            )
            
            # A API da Lusófona costuma enviar uma lista de 'unidades_curriculares'
            ucs = dados.get('unidades_curriculares', [])
            
            for uc_data in ucs:
                # O update_or_create evita duplicados se correres o script 2 vezes
                UnidadeCurricular.objects.update_or_create(
                    nome=uc_data['nome'],
                    licenciatura=licenciatura,
                    defaults={
                        'ects': uc_data.get('ects', 6),
                        'ano': uc_data.get('ano_curricular', 1),
                        'docente': "A designar" # A API nem sempre expõe o docente diretamente
                    }
                )
            print("Importação concluída com sucesso!")
        else:
            print(f"Erro na API: {response.status_code}")
            
    except Exception as e:
        print(f"Erro na ligação: {e}")
            
    return redirect('portfolio:home')