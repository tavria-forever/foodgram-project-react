# Generated by Django 2.2.16 on 2022-12-11 17:10

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Follow',
            fields=[
                (
                    'id',
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name='ID',
                    ),
                ),
            ],
            options={
                'verbose_name': 'Подписка',
                'verbose_name_plural': 'Подписки',
            },
        ),
        migrations.RemoveConstraint(
            model_name='user',
            name='unique_username_email',
        ),
        migrations.AddConstraint(
            model_name='user',
            constraint=models.UniqueConstraint(
                fields=('username', 'email'), name='user_unique_username_email'
            ),
        ),
        migrations.AddField(
            model_name='follow',
            name='author_id',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='following',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddField(
            model_name='follow',
            name='user_id',
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name='follower',
                to=settings.AUTH_USER_MODEL,
            ),
        ),
        migrations.AddConstraint(
            model_name='follow',
            constraint=models.UniqueConstraint(
                fields=('user_id', 'author_id'),
                name='follow_user_author_unique',
            ),
        ),
    ]
