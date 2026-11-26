from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name='StoredFile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True, verbose_name='Путь')),
                ('content', models.BinaryField(verbose_name='Содержимое')),
                ('content_type', models.CharField(blank=True, max_length=100, verbose_name='MIME-тип')),
                ('size', models.PositiveBigIntegerField(default=0, verbose_name='Размер, байт')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Загружен')),
            ],
            options={
                'verbose_name': 'файл в БД',
                'verbose_name_plural': 'файлы в БД',
                'ordering': ['name'],
            },
        ),
    ]
