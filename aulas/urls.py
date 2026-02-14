from django.urls import path
from . import views

urlpatterns = [
    # Rota para a página inicial (lista de aulas)
    path('', views.home, name='home'), 
    
    # Rota para ver o detalhe de uma aula específica
    path('licao/<int:id>/', views.licao_detalhe, name='licao_detalhe'), 
]