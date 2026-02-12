from django.shortcuts import render, get_object_or_404
from .models import Categoria, Publicacao

def index_guia(request):
    # Pega todas as categorias para mostrar os cartões
    categorias = Categoria.objects.all()
    return render(request, 'guia/index.html', {'categorias': categorias})

def detalhe_categoria(request, id):
    # Pega a categoria clicada e filtra as publicações dela
    categoria = get_object_or_404(Categoria, id=id)
    publicacoes = Publicacao.objects.filter(categoria=categoria)
    return render(request, 'guia/categoria.html', {'categoria': categoria, 'publicacoes': publicacoes})