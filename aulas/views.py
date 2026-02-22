from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.utils import timezone
import unicodedata # <--- NOSSA NOVA FERRAMENTA MÁGICA!

from guia.models import Publicacao
from .models import Licao
from .forms import CadastroSeguroForm

# --- FUNÇÃO QUE ARRANCA ACENTOS E DEIXA TUDO MINÚSCULO ---
def remover_acentos(texto):
    if not texto:
        return ""
    # Transforma "Apresentação" em "apresentacao"
    texto = unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8')
    return texto.lower()

# --- NOSSO CÉREBRO AGORA É 100% ACESSÍVEL ---
def home(request):
    busca = request.GET.get('busca')
    hoje = timezone.now().date() 
    
    if busca:
        # 1. Limpa a palavra que o usuário digitou
        busca_limpa = remover_acentos(busca)
        
        # 2. Varre as Aulas ignorando acentos e letras maiúsculas/minúsculas
        todas_licoes = Licao.objects.all()
        licoes = [aula for aula in todas_licoes if busca_limpa in remover_acentos(aula.titulo) or busca_limpa in remover_acentos(aula.conteudo)]
        
        # 3. Varre o Guia de Serviços ignorando acentos e letras maiúsculas/minúsculas
        todas_pubs = Publicacao.objects.all()
        publicacoes = [pub for pub in todas_pubs if busca_limpa in remover_acentos(pub.titulo) or busca_limpa in remover_acentos(pub.conteudo)]
    else:
        # Se não pesquisou nada, mostra o padrão
        licoes = Licao.objects.all()
        publicacoes = None
    
    return render(request, 'home.html', {
        'licoes': licoes, 
        'publicacoes': publicacoes, 
        'hoje': hoje
    })

# ... (aqui embaixo continua as suas funções licao_detalhe e cadastro, deixe elas como estão) ...
def licao_detalhe(request, id):
    licao = get_object_or_404(Licao, id=id)
    return render(request, 'licao_detalhe.html', {'licao': licao})

def cadastro(request):
    if request.method == 'POST':
        form = CadastroSeguroForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user) 
            return redirect('home')
    else:
        form = CadastroSeguroForm()
    
    return render(request, 'cadastro.html', {'form': form})