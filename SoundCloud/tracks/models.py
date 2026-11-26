from django.db import models
from django.contrib.auth.models import User

class Track(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="Исполнитель")
    title = models.CharField(max_length=150, verbose_name="Название трека")
    description = models.TextField(blank=True, verbose_name="Описание")
    cover = models.ImageField(upload_to='covers/', blank=True, null=True, verbose_name="Обложка")
    audio_file = models.FileField(upload_to='tracks/', verbose_name="Аудиофайл (MP3/WAV)")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Дата загрузки")

    def __str__(self):
        return f"{self.author.username} - {self.title}"
