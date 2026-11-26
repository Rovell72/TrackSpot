"""Файловое хранилище Django, которое кладёт файлы в таблицу core_storedfile (db.sqlite3).

Подключается через STORAGES['default'] в settings.py, поэтому ImageField / FileField
в моделях (аватарки, обложки, аудио) работают как раньше, но байты лежат в базе.
"""
import mimetypes
from urllib.parse import urljoin

from django.conf import settings
from django.core.files.base import ContentFile
from django.core.files.storage import Storage
from django.utils.encoding import filepath_to_uri


class DatabaseStorage(Storage):

    @staticmethod
    def _norm(name):
        # В БД всегда прямые слэши (на Windows os.path.join даёт обратные)
        return str(name).replace('\\', '/').lstrip('/')

    @staticmethod
    def _model():
        from .models import StoredFile
        return StoredFile

    def _open(self, name, mode='rb'):
        if set(mode) & set('wa+x'):
            raise ValueError("DatabaseStorage поддерживает только чтение через open().")
        name = self._norm(name)
        try:
            data = self._model().objects.values_list('content', flat=True).get(name=name)
        except self._model().DoesNotExist:
            raise FileNotFoundError(name)
        return ContentFile(bytes(data), name=name)

    def _save(self, name, content):
        name = self._norm(name)
        if hasattr(content, 'seek'):
            try:
                content.seek(0)
            except Exception:
                pass
        data = b''.join(content.chunks()) if hasattr(content, 'chunks') else content.read()

        content_type = (
            mimetypes.guess_type(name)[0]
            or getattr(content, 'content_type', None)
            or 'application/octet-stream'
        )
        self._model().objects.create(
            name=name,
            content=data,
            content_type=content_type[:100],
            size=len(data),
        )
        return name

    def get_available_name(self, name, max_length=None):
        name = super().get_available_name(self._norm(name), max_length)
        return self._norm(name)

    def exists(self, name):
        return self._model().objects.filter(name=self._norm(name)).exists()

    def delete(self, name):
        if name:
            self._model().objects.filter(name=self._norm(name)).delete()

    def size(self, name):
        try:
            return self._model().objects.values_list('size', flat=True).get(name=self._norm(name))
        except self._model().DoesNotExist:
            raise FileNotFoundError(name)

    def url(self, name):
        base = settings.MEDIA_URL
        if not base.endswith('/'):
            base += '/'
        return urljoin(base, filepath_to_uri(self._norm(name)))
