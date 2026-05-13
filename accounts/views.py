
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from .forms import RegistroForm
from django.core.mail import send_mail
from django.contrib.auth.models import User
from django.contrib import messages
import uuid

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], 
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('portfolio:home') # Altera para a tua página inicial
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('portfolio:home')

def registo_view(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = RegistroForm()
    return render(request, 'accounts/registo.html', {'form': form})

from django.contrib.auth.models import Group

def registo(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Adicionar ao grupo autores
            grupo_autores = Group.objects.get(name='autores')
            user.groups.add(grupo_autores)
            login(request, user)
            return redirect('portfolio:home')
     

def solicitar_link_magico(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        try:
            user = User.objects.get(email=email)
            # Gerar um token único e guardar na sessão
            token = str(uuid.uuid4())
            request.session['magic_token'] = token
            request.session['magic_user_id'] = user.id
            
            # Criar o link completo
            link = request.build_absolute_uri(f'/accounts/magic-login/{token}/')
            
            # "Enviar" o e-mail (aparecerá no terminal)
            send_mail(
                'O teu Link Mágico',
                f'Clica no link para entrar: {link}',
                'noreply@portfolio.com',
                [email],
            )
            messages.success(request, "Link enviado! Verifica o teu e-mail (terminal).")
        except User.DoesNotExist:
            messages.error(request, "E-mail não encontrado.")
            
    return render(request, 'accounts/solicitar_link.html')

# View que processa o clique no link
def validar_link_magico(request, token):
    session_token = request.session.get('magic_token')
    user_id = request.session.get('magic_user_id')
    
    if session_token == token and user_id:
        user = User.objects.get(id=user_id)
        login(request, user)
        del request.session['magic_token'] # Limpar token após uso
        return redirect('portfolio:home')
    
    messages.error(request, "Link inválido ou expirado.")
    return redirect('accounts:login')