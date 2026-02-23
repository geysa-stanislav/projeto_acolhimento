from django.shortcuts import render, get_object_or_404
from .models import Categoria, Publicacao

def index_guia(request):
    categorias = Categoria.objects.all()
    return render(request, 'guia/index.html', {'categorias': categorias})

# CÓDIGO CORRETO:
def detalhe_categoria(request, id):
    categoria = get_object_or_404(Categoria, id=id)
    
    # Agora ele filtra e pega SÓ as publicações que pertencem a essa categoria!
    publicacoes = Publicacao.objects.filter(categoria=categoria) 
    
    return render(request, 'categoria.html', {'categoria': categoria, 'publicacoes': publicacoes})