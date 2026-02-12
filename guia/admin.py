from django.contrib import admin
from .models import Categoria, Publicacao

@admin.register(Categoria)
class CategoriaAdmin(admin.ModelAdmin):
    list_display = ('nome',)

@admin.register(Publicacao)
class PublicacaoAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'categoria', 'data_criacao', 'autor')
    list_filter = ('categoria', 'data_criacao')
    search_fields = ('titulo', 'conteudo')
