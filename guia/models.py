from django.db import models
from django.contrib.auth.models import User
# 1. ADICIONE O IMPORT AQUI NO TOPO
from ckeditor_uploader.fields import RichTextUploadingField

class Categoria(models.Model):
    nome = models.CharField(max_length=50)
    
    def __str__(self):
        return self.nome

class Publicacao(models.Model):
    titulo = models.CharField(max_length=200)
    
    # 2. SUBSTITUA O TEXTFIELD PELO RICHTEXTFIELD AQUI
    conteudo = RichTextUploadingField()
    
    categoria = models.ForeignKey(Categoria, on_delete=models.CASCADE)
    link_mapa = models.URLField(blank=True, null=True, help_text="Link do Google Maps")
    imagem = models.ImageField(upload_to='guia_imagens/', blank=True, null=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    autor = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.titulo