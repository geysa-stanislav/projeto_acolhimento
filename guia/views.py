from django.shortcuts import render, get_object_or_404
from .models import Categoria, Publicacao

def index_guia(request):
    categorias = Categoria.objects.all()
    return render(request, 'guia/index.html', {'categorias': categorias})

def detalhe_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    # Garante que as publicações sejam encontradas para a página não dar erro
    publicacoes = Publicacao.objects.filter(categoria=categoria)
    return render(request, 'guia/categoria.html', {'categoria': categoria, 'publicacoes': publicacoes})