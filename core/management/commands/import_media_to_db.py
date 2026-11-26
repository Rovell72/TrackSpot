import mimetypes
from pathlib import Path

from django.conf import settings
from django.core.management.base import BaseCommand

from core.models import StoredFile
from tracks.models import Track
from users.models import Profile


class Command(BaseCommand):
    help = (
        "Переносит уже загруженные файлы (аватарки, обложки, аудио) из папки media/ "
        "в таблицу core_storedfile внутри db.sqlite3."
    )

    def add_arguments(self, parser):
        parser.add_argument(
            '--delete-files', action='store_true',
            help="Удалить файл из media/ после успешного переноса.",
        )

    def handle(self, *args, **options):
        sources = [
            (Profile, 'avatar'),
            (Track, 'cover'),
            (Track, 'audio_file'),
        ]
        root = Path(settings.MEDIA_ROOT)
        imported = skipped = missing = 0

        for model, field in sources:
            for obj in model.objects.exclude(**{field: ''}).exclude(**{f'{field}__isnull': True}):
                name = getattr(obj, field).name.replace('\\', '/')

                if StoredFile.objects.filter(name=name).exists():
                    skipped += 1
                    continue

                path = root / name
                if not path.is_file():
                    missing += 1
                    self.stderr.write(self.style.WARNING(
                        f"[нет файла] {model.__name__}#{obj.pk}.{field}: {path}"
                    ))
                    continue

                data = path.read_bytes()
                StoredFile.objects.create(
                    name=name,
                    content=data,
                    content_type=mimetypes.guess_type(name)[0] or 'application/octet-stream',
                    size=len(data),
                )
                imported += 1
                self.stdout.write(f"[перенесён] {name} ({len(data)} байт)")

                if options['delete_files']:
                    path.unlink()

        self.stdout.write(self.style.SUCCESS(
            f"Готово. Перенесено: {imported}, уже в БД: {skipped}, не найдено на диске: {missing}."
        ))
