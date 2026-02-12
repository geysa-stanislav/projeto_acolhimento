from django.shortcuts import render, get_object_or_404, redirect  # <--- O redirect está aqui!
from .models import Licao
from django.utils import timezone
from django.db.models import Q
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm # <--- E o formulário aqui
# --- FUNÇÃO DA PÁGINA INICIAL (COM BUSCA) ---
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
 
    # 2. BLOQUEIE A ENTRADA AQUI:
@login_required(login_url='login')
def detalhe_licao(request, id):
    licao = get_object_or_404(Licao, id=id)
    return render(request, 'licao_detalhe.html', {'licao': licao})

# --- FUNÇÃO DA PÁGINA DA AULA (ELA TEM QUE ESTAR AQUI!) ---
def detalhe_licao(request, id):
    licao = get_object_or_404(Licao, id=id)
    return render(request, 'licao_detalhe.html', {'licao': licao})
def criar_conta(request):
    if request.method == 'POST':
        # Se o usuário mandou dados, cria o formulário com esses dados
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save() # Salva no banco de dados
            return redirect('login') # Manda ir fazer login
    else:
        # Se ele só entrou na página, mostra o formulário vazio
        form = UserCreationForm()
    
    return render(request, 'cadastro.html', {'form': form})