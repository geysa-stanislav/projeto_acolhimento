from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.utils import timezone
from django.db.models import Q
from .models import Licao

# --- 1. PÁGINA INICIAL (PROTEGIDA) ---
# O @login_required impede que entrem aqui sem senha
@login_required
def home(request):
    licoes = Licao.objects.all().order_by('data_lancamento')
    
    # Lógica da Busca
    termo_busca = request.GET.get('busca')
    if termo_busca:
        licoes = licoes.filter(
            Q(titulo__icontains=termo_busca) | Q(conteudo__icontains=termo_busca)
        )
    
    hoje = timezone.now().date()
    return render(request, 'home.html', {'licoes': licoes, 'hoje': hoje})

# --- 2. PÁGINA DA LIÇÃO (PROTEGIDA) ---
# Aqui também tem cadeado
@login_required
def detalhe_licao(request, id):
    licao = get_object_or_404(Licao, id=id)
    return render(request, 'licao_detalhe.html', {'licao': licao})

# --- 3. PÁGINA DE CRIAR CONTA (PÚBLICA) ---
# ATENÇÃO: Essa NÃO PODE ter @login_required, senão ninguém consegue se cadastrar!
def criar_conta(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    
    return render(request, 'cadastro.html', {'form': form})