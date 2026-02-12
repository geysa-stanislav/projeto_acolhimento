from django.contrib import admin
from .models import Licao

# Isso coloca a tabela "Licao" dentro do painel administrativo
admin.site.register(Licao)
