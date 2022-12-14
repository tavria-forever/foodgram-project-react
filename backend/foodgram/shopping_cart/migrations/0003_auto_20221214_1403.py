# Generated by Django 2.2.16 on 2022-12-14 14:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopping_cart', '0002_auto_20221211_1708'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='shoppingorder',
            name='shopping_order_user_recipe_unique',
        ),
        migrations.RenameField(
            model_name='shoppingorder',
            old_name='recipe_id',
            new_name='recipe',
        ),
        migrations.RenameField(
            model_name='shoppingorder',
            old_name='user_id',
            new_name='user',
        ),
        migrations.AddConstraint(
            model_name='shoppingorder',
            constraint=models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='shopping_order_user_recipe_unique',
            ),
        ),
    ]
