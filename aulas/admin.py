from django.contrib import admin
from django.contrib.admin.models import LogEntry # <-- A mágica importada aqui
from .models import Licao

# --- CONFIGURAÇÃO DAS LIÇÕES (O QUE VOCÊ JÁ TINHA) ---
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

# --- O NOVO CÓDIGO DO RAIO-X (AUDITORIA DE ADMINS) ---
@admin.register(LogEntry)
class LogEntryAdmin(admin.ModelAdmin):
    # Mostra: Data/Hora, Quem fez, Onde fez, Qual arquivo, e O que fez (Adicionou/Editou/Apagou)
    list_display = ['action_time', 'user', 'content_type', 'object_repr', 'action_flag']
    
    # Cria filtros na lateral por usuário e por tipo de ação
    list_filter = ['user', 'action_flag']
    
    # Barra de pesquisa
    search_fields = ['object_repr', 'change_message']

    # Bloqueia a edição dessa tela (ninguém pode apagar provas do que fez! rs)
    def has_add_permission(self, request): return False
    def has_change_permission(self, request, obj=None): return False
    def has_delete_permission(self, request, obj=None): return False