from django.contrib import admin
from .models import Licao

@admin.register(Licao)
class LicaoAdmin(admin.ModelAdmin):
    # Colunas que aparecerão na lista (muito mais profissional)
    list_display = ('titulo', 'data_lancamento', 'visualizar_no_site')
    
    # Adiciona uma barra de busca por título ou conteúdo
    search_fields = ('titulo', 'conteudo')
    
    # Adiciona filtros laterais por data
    list_filter = ('data_lancamento',)
    
    # Permite editar a data direto na lista sem precisar abrir a lição
    list_editable = ('data_lancamento',)

    def visualizar_no_site(self, obj):
        # Cria um link rápido para o admin ver como está a lição no site
        return "Visualizar"
