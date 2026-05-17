from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('licao/<int:id>/', views.licao_detalhe, name='licao_detalhe'),
    path('cadastro/', views.cadastro, name='cadastro'), # Rota liberada!
    path('ia/tutor/', views.tutor_ia, name='tutor_ia'), # Rota NOVA da Inteligência Artificial
]