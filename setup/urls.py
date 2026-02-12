from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

# Importamos as views da home e do login/cadastro
from aulas.views import home, detalhe_licao, criar_conta
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # --- ROTA DA PÁGINA INICIAL ---
    path('', home, name='home'),
    
    # --- ROTAS DE AULAS ---
    path('licao/<int:id>/', detalhe_licao, name='detalhe_licao'),
    
    # --- ROTAS DE USUÁRIO (Login/Cadastro/Sair) ---
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('cadastro/', criar_conta, name='cadastro'),

    # --- ROTA DO GUIA (NOVA!) ---
    # Tudo que for http://site/guia/... vai para o app guia
    path('guia/', include('guia.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)