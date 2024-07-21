from django.urls import path

from restaurant_kitchen.views import (
    index,
    DishTypeListView,
    DishListView,
    CookListView,
    dish_detail_view
)

urlpatterns = [
    path("", index, name="index"),
    path("dish-types/", DishTypeListView.as_view(), name="dish-type-list"),
    path("dish/", DishListView.as_view(), name="dish-list"),
    path("cook/", CookListView.as_view(), name="cook-list"),
    path("dish/<int:pk>/", dish_detail_view, name="dish-detail"),

]

app_name = "restaurant_kitchen"
