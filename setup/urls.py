from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
# Importamos as views de autenticação padrão
from django.contrib.auth import views as auth_views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('aulas.urls')),
    path('guia/', include('guia.urls')),
    path('ckeditor/', include('ckeditor_uploader.urls')),

    # ROTAS DE LOGIN E LOGOUT (O que resolve o seu erro)
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)