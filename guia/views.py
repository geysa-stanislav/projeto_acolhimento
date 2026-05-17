from django.shortcuts import render, get_object_or_404
from .models import Categoria, Publicacao

def index_guia(request):
    categorias = Categoria.objects.all()
    return render(request, 'guia/index.html', {'categorias': categorias})

def detalhe_categoria(request, id):
    # Pega apenas a categoria clicada
    categoria = get_object_or_404(Categoria, id=id)

    # Removemos o filtro daqui. Vamos mandar SÓ a categoria para o HTML.
    return render(request, 'guia/categoria.html', {'categoria': categoria})