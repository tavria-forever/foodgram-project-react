# Generated by Django 2.2.16 on 2022-12-11 20:01

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0004_auto_20221211_1851'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={
                'ordering': ('name', 'measurement_unit'),
                'verbose_name': 'Ингридиент',
                'verbose_name_plural': 'Ингридиенты',
            },
        ),
    ]
