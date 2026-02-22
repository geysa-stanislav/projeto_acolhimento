import unicodedata
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.utils import timezone
from .models import Licao
from .forms import CadastroSeguroForm
from guia.models import Publicacao

# Função para ignorar acentos na busca
def remover_acentos(texto):
    if not texto: return ""
    return unicodedata.normalize('NFKD', str(texto)).encode('ASCII', 'ignore').decode('utf-8').lower()

def home(request):
    busca = request.GET.get('busca')
    hoje = timezone.now().date()
    if busca:
        busca_limpa = remover_acentos(busca)
        licoes = [l for l in Licao.objects.all() if busca_limpa in remover_acentos(l.titulo) or busca_limpa in remover_acentos(l.conteudo)]
        publicacoes = [p for p in Publicacao.objects.all() if busca_limpa in remover_acentos(p.titulo) or busca_limpa in remover_acentos(p.conteudo)]
    else:
        licoes = Licao.objects.all()
        publicacoes = None
    return render(request, 'home.html', {'licoes': licoes, 'publicacoes': publicacoes, 'hoje': hoje})

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