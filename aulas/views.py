from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import Licao
from django.utils import timezone

def home(request):
    busca = request.GET.get('busca')
    if busca:
        licoes = Licao.objects.filter(titulo__icontains=busca)
    else:
        licoes = Licao.objects.all()
    
    hoje = timezone.now().date() 
    
    return render(request, 'home.html', {
        'licoes': licoes, 
        'hoje': hoje
    })

def licao_detalhe(request, id):
    licao = get_object_or_404(Licao, id=id)
    return render(request, 'licao_detalhe.html', {'licao': licao})

# --- NOVA FUNÇÃO DE CADASTRO ---
def cadastro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Esta linha já faz o login automático assim que o aluno cria a conta!
            login(request, user) 
            return redirect('home')
    else:
        form = UserCreationForm()
    
    return render(request, 'cadastro.html', {'form': form})