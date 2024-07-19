from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
from django.db import models
from RestaurantKitchenService import settings


class DishType(models.Model):
    name = models.CharField(max_length=255, unique=True)

    def __str__(self) -> str:
        return self.name


class Cook(AbstractUser):
    years_of_experience = models.IntegerField(
        null=False,
        blank=False,
        validators=[MinValueValidator(0)]
    )

    class Meta:
        verbose_name = "Cook"

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


class Dish(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    dish_type = models.ForeignKey(DishType, on_delete=models.CASCADE)
    cooks = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name="dishes")

    class Meta:
        ordering = ("name", )

    def __str__(self) -> str:
        return self.name
