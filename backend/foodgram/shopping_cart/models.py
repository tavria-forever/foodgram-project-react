from django.db import models

from recipes.models import Recipe
from users.models import User


class ShoppingOrder(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='shopping_orders'
    )
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, related_name='shopping_orders'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='shopping_order_user_recipe_unique',
            ),
        ]
        verbose_name = 'Заказ на покупку'
        verbose_name_plural = 'Заказы на покупку'

    def __str__(self):
        return (
            f'Пользователь {self.user} добавил в корзину рецепт {self.recipe}'
        )
