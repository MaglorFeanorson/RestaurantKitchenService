from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from restaurant_kitchen.models import (
    DishType,
    Cook,
    Dish
)


class ModelTests(TestCase):

    def setUp(self):
        self.dish_type = DishType.objects.create(
            name="Dessert"
        )

        self.cook = get_user_model().objects.create_user(
            username="testcook",
            password="password123",
            first_name="John",
            last_name="Doe",
            years_of_experience=5
        )

        self.dish = Dish.objects.create(
            name="Cake",
            description="Delicious chocolate cake",
            price=5.50,
            dish_type=self.dish_type,
        )
        self.dish.cooks.add(self.cook)

    def test_dish_type_str_representation(self):
        self.assertEqual(str(self.dish_type), self.dish_type.name)

    def test_cook_str_representation(self):
        self.assertEqual(
            str(self.cook), f"{self.cook.first_name} {self.cook.last_name}"
        )

    def test_dish_str_representation(self):
        self.assertEqual(str(self.dish), self.dish.name)

    def test_create_cook_with_years_of_experience(self):
        username = "newcook"
        password = "cookpassword"
        cook = get_user_model().objects.create_user(
            username=username,
            password=password,
            first_name="Jane",
            last_name="Smith",
            years_of_experience=3
        )
        self.assertEqual(cook.username, username)
        self.assertEqual(cook.years_of_experience, 3)
        self.assertTrue(cook.check_password(password))

    def test_get_absolute_url_cook(self):
        expected_url = reverse(
            "restaurant_kitchen:cook-detail",
            kwargs={"pk": self.cook.pk}
        )
        self.assertEqual(self.cook.get_absolute_url(), expected_url)

    def test_get_absolute_url_dish(self):
        expected_url = reverse(
            "restaurant_kitchen:dish-detail",
            kwargs={"pk": self.dish.pk}
        )
        self.assertEqual(self.dish.get_absolute_url(), expected_url)


class PublicDishTypeTests(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("restaurant_kitchen:dish-type-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateDishTypeTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(name="Main Course")

    def test_retrieve_dish_types(self):
        response = self.client.get(
            reverse("restaurant_kitchen:dish-type-list")
        )
        self.assertEqual(response.status_code, 200)
        dish_types = DishType.objects.all()
        self.assertEqual(
            list(response.context["dish_type_list"]), list(dish_types)
        )
        self.assertTemplateUsed(
            response, "restaurant_kitchen/dish_type_list.html"
        )

    def test_search_dish_type(self):
        response = self.client.get(
            reverse("restaurant_kitchen:dish-type-list"), {"name": "Main"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Main Course")
        self.assertNotContains(response, "Dessert")


class PublicCookTests(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("restaurant_kitchen:cook-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateCookTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_login(self.user)
        self.cook = get_user_model().objects.create_user(
            username="cook1",
            password="password123",
            first_name="Cook",
            last_name="One",
            years_of_experience=4
        )

    def test_retrieve_cooks(self):
        response = self.client.get(reverse("restaurant_kitchen:cook-list"))
        self.assertEqual(response.status_code, 200)
        cooks = Cook.objects.all()
        self.assertEqual(list(response.context["cook_list"]), list(cooks))
        self.assertTemplateUsed(response, "restaurant_kitchen/cook_list.html")


class PublicDishTests(TestCase):
    def test_login_required(self):
        res = self.client.get(reverse("restaurant_kitchen:dish-list"))
        self.assertNotEqual(res.status_code, 200)


class PrivateDishTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_login(self.user)
        self.dish_type = DishType.objects.create(name="Main Course")
        self.dish = Dish.objects.create(
            name="Steak",
            description="Grilled steak",
            price=15.00,
            dish_type=self.dish_type
        )

    def test_retrieve_dishes(self):
        response = self.client.get(reverse("restaurant_kitchen:dish-list"))
        self.assertEqual(response.status_code, 200)
        dishes = Dish.objects.select_related("dish_type").all()
        self.assertEqual(list(response.context["dish_list"]), list(dishes))
        self.assertTemplateUsed(response, "restaurant_kitchen/dish_list.html")

    def test_search_dish(self):
        response = self.client.get(
            reverse("restaurant_kitchen:dish-list"), {"name": "Steak"}
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Steak")
        self.assertNotContains(response, "Cake")
