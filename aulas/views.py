import unicodedata
from django.shortcuts import render
from .models import Licao
from guia.models import Publicacao 
from django.utils import timezone

# Função para ignorar acentos na busca
def remover_acentos(texto):
    if not texto: return ""
    return unicodedata.normalize('NFKD', texto).encode('ASCII', 'ignore').decode('utf-8').lower()

def home(request):
    busca = request.GET.get('busca')
    hoje = timezone.now().date()
    if busca:
        busca_limpa = remover_acentos(busca)
        # Busca nas Aulas
        todas_licoes = Licao.objects.all()
        licoes = [l for l in todas_licoes if busca_limpa in remover_acentos(l.titulo) or busca_limpa in remover_acentos(l.conteudo)]
        # Busca no Guia de Serviços (ACHA O CARTÃO SUS AQUI)
        todas_pubs = Publicacao.objects.all()
        publicacoes = [p for p in todas_pubs if busca_limpa in remover_acentos(p.titulo) or busca_limpa in remover_acentos(p.conteudo)]
    else:
        licoes = Licao.objects.all()
        publicacoes = None
    return render(request, 'home.html', {'licoes': licoes, 'publicacoes': publicacoes, 'hoje': hoje})

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