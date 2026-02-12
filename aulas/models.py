from django.db import models
from django.utils import timezone

class Licao(models.Model):
    titulo = models.CharField(max_length=200)
    conteudo = models.TextField()
    video_url = models.URLField(blank=True, null=True)
    imagem = models.ImageField(upload_to='imagens_licoes/', blank=True, null=True)
    arquivo_pdf = models.FileField(upload_to='atividades/', blank=True, null=True)
    data_lancamento = models.DateField(default=timezone.now, help_text="Data que a aula será liberada")
    data_publicacao = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Lição"
        verbose_name_plural = "Lições"
        ordering = ['data_lancamento']

    def __str__(self):
        return self.titulo

    def get_video_embed(self):
        url = self.video_url
        if not url: return ""
        video_id = ""
        if "youtu.be/" in url:
            try: video_id = url.split("youtu.be/")[1]
            except IndexError: pass
        elif "watch?v=" in url:
            try: video_id = url.split("watch?v=")[1]
            except IndexError: pass
        if video_id:
            if "&" in video_id: video_id = video_id.split("&")[0]
            if "?" in video_id: video_id = video_id.split("?")[0]
            return f"https://www.youtube.com/embed/{video_id}"
        return url