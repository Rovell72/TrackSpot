"""Чистит БД от «осиротевших» файлов: при удалении записи или замене файла.

Раньше файлы просто копились в media/; теперь они лежат в базе, и мусор
раздувал бы db.sqlite3.
"""
from django.apps import apps
from django.db import transaction
from django.db.models.signals import post_delete, pre_save

FILE_FIELDS = {
    'tracks.Track': ('cover', 'audio_file'),
    'users.Profile': ('avatar',),
}


def _delete_after_commit(storage, name):
    transaction.on_commit(lambda: storage.delete(name))


def _make_handlers(fields):
    def on_pre_save(sender, instance, **kwargs):
        if not instance.pk:
            return
        old = sender.objects.filter(pk=instance.pk).first()
        if old is None:
            return
        for field in fields:
            old_file = getattr(old, field)
            new_file = getattr(instance, field)
            if old_file and old_file.name != (new_file.name if new_file else None):
                _delete_after_commit(old_file.storage, old_file.name)

    def on_post_delete(sender, instance, **kwargs):
        for field in fields:
            f = getattr(instance, field)
            if f:
                _delete_after_commit(f.storage, f.name)

    return on_pre_save, on_post_delete


def connect():
    for label, fields in FILE_FIELDS.items():
        model = apps.get_model(label)
        on_pre_save, on_post_delete = _make_handlers(fields)
        pre_save.connect(on_pre_save, sender=model, weak=False, dispatch_uid=f'{label}.files.pre_save')
        post_delete.connect(on_post_delete, sender=model, weak=False, dispatch_uid=f'{label}.files.post_delete')
