# Generated by Django 2.2.16 on 2022-12-21 07:34

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0009_auto_20221217_2151'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favouriterecipe',
            options={
                'ordering': ('-id',),
                'verbose_name': 'Рецепт в избранном',
                'verbose_name_plural': 'Рецепты в избранном',
            },
        ),
    ]
