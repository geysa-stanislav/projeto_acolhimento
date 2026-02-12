from django.urls import path
from . import views

urlpatterns = [
    # Página inicial do guia (lista de categorias)
    path('', views.index_guia, name='index_guia'),
    
    # Página de detalhes (quando clica numa categoria)
    path('categoria/<int:id>/', views.detalhe_categoria, name='detalhe_categoria'),
]