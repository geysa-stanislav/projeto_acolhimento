from django.shortcuts import render, get_object_or_404
from .models import Licao
from django.utils import timezone

def home(request):
    # Mantém sua função de busca original
    busca = request.GET.get('busca')
    if busca:
        licoes = Licao.objects.filter(titulo__icontains=busca)
    else:
        licoes = Licao.objects.all()
    
    # Mantém a variável hoje para a trava de data que você criou
    hoje = timezone.now().date() 
    
    return render(request, 'home.html', {
        'licoes': licoes, 
        'hoje': hoje
    })

def licao_detalhe(request, id):
    licao = get_object_or_404(Licao, id=id)
    return render(request, 'licao_detalhe.html', {'licao': licao})