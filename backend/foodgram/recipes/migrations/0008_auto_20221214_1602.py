# Generated by Django 2.2.16 on 2022-12-14 16:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0007_auto_20221214_1408'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favouriterecipe',
            options={'ordering': ('-id',)},
        ),
        migrations.AlterModelOptions(
            name='measurementunit',
            options={
                'ordering': ('-name',),
                'verbose_name': 'Единица измерения',
                'verbose_name_plural': 'Единицы измерения',
            },
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={
                'ordering': ('-id',),
                'verbose_name': 'Рецепт',
                'verbose_name_plural': 'Рецепты',
            },
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={
                'ordering': ('-name',),
                'verbose_name': 'Тег',
                'verbose_name_plural': 'Теги',
            },
        ),
    ]
