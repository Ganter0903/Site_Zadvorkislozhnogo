# Generated by Django 5.2.1 on 2025-06-01 17:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Zadvorkislozhnogo', '0004_user_avatar'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='audiobook',
            options={'verbose_name': 'Аудиокнига', 'verbose_name_plural': 'Аудиокниги'},
        ),
        migrations.AlterModelOptions(
            name='poem',
            options={'verbose_name': 'Стих', 'verbose_name_plural': 'Стихи'},
        ),
        migrations.AlterModelOptions(
            name='story',
            options={'verbose_name': 'Рассказ', 'verbose_name_plural': 'Рассказы'},
        ),
    ]
