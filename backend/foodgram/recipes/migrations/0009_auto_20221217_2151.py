# Generated by Django 2.2.16 on 2022-12-17 21:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0008_auto_20221214_1602'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ingredient',
            options={
                'ordering': ('name', 'measurement_unit'),
                'verbose_name': 'Ингредиент',
                'verbose_name_plural': 'Ингредиенты',
            },
        ),
    ]