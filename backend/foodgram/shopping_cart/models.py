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
        ordering = ('-id',)
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='shopping_order_user_recipe_unique',
            ),
        ]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Списки покупок'

    def __str__(self):
        return f'pk: {self.id} пользователь {self.user} добавил в корзину рецепт {self.recipe}'
