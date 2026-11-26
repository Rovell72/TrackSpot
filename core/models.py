from django.db import models


class StoredFile(models.Model):
    """Файл (аватарка, обложка, аудио), хранящийся прямо в db.sqlite3."""

    name = models.CharField(max_length=255, unique=True, verbose_name="Путь")
    content = models.BinaryField(verbose_name="Содержимое")
    content_type = models.CharField(max_length=100, blank=True, verbose_name="MIME-тип")
    size = models.PositiveBigIntegerField(default=0, verbose_name="Размер, байт")
    created_at = models.DateTimeField(auto_now_add=True, verbose_name="Загружен")

    class Meta:
        ordering = ['name']
        verbose_name = "файл в БД"
        verbose_name_plural = "файлы в БД"

    def __str__(self):
        return self.name
