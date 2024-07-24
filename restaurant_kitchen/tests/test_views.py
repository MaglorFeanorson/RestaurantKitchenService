from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from restaurant_kitchen.models import (
    Cook,
    Dish,
    DishType
)

COOK_LIST_URL = reverse("restaurant_kitchen:cook-list")
DISH_LIST_URL = reverse("restaurant_kitchen:dish-list")
DISH_TYPE_LIST_URL = reverse("restaurant_kitchen:dish-type-list")


class PublicCookTest(TestCase):
    def test_login_required(self):
        res = self.client.get(COOK_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateCookTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_login(self.user)
        Cook.objects.create(
            username="cook1",
            first_name="John",
            last_name="Doe",
            years_of_experience=5
        )
        Cook.objects.create(
            username="cook2",
            first_name="Jane",
            last_name="Smith",
            years_of_experience=3
        )

    def test_retrieve_cooks(self):
        response = self.client.get(COOK_LIST_URL)
        self.assertEqual(response.status_code, 200)
        cooks = Cook.objects.all()
        self.assertEqual(list(response.context["cook_list"]), list(cooks))
        self.assertTemplateUsed(response, "restaurant_kitchen/cook_list.html")

    def test_search_cook(self):
        response = self.client.get(COOK_LIST_URL, {"username": "cook1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "cook1")
        self.assertNotContains(response, "cook2")


class PublicDishTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DISH_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDishTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_login(self.user)
        dish_type = DishType.objects.create(name="Appetizer")
        self.dish1 = Dish.objects.create(
            name="Dish1",
            description="Description1",
            price=10.00,
            dish_type=dish_type
        )
        self.dish2 = Dish.objects.create(
            name="Dish2",
            description="Description2",
            price=20.00,
            dish_type=dish_type
        )

    def test_retrieve_dishes(self):
        response = self.client.get(DISH_LIST_URL)
        self.assertEqual(response.status_code, 200)
        dishes = Dish.objects.select_related("dish_type").all()
        self.assertEqual(list(response.context["dish_list"]), list(dishes))
        self.assertTemplateUsed(response, "restaurant_kitchen/dish_list.html")

    def test_search_dish(self):
        response = self.client.get(DISH_LIST_URL, {"name": "Dish1"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Dish1")
        self.assertNotContains(response, "Dish2")


class PublicDishTypeTest(TestCase):
    def test_login_required(self):
        res = self.client.get(DISH_TYPE_LIST_URL)
        self.assertNotEqual(res.status_code, 200)


class PrivateDishTypeTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_login(self.user)
        DishType.objects.create(name="Appetizer")
        DishType.objects.create(name="Main Course")

    def test_retrieve_dish_types(self):
        response = self.client.get(DISH_TYPE_LIST_URL)
        self.assertEqual(response.status_code, 200)
        dish_types = DishType.objects.all()
        self.assertEqual(
            list(response.context["dish_type_list"]), list(dish_types)
        )
        self.assertTemplateUsed(
            response, "restaurant_kitchen/dish_type_list.html"
        )

    def test_search_dish_type(self):
        response = self.client.get(DISH_TYPE_LIST_URL, {"name": "Appetizer"})
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Appetizer")
        self.assertNotContains(response, "Main Course")


class PrivateIndexViewTest(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user(
            username="testuser",
            password="testpass123",
        )
        self.client.force_login(self.user)

    def test_index_view(self):
        response = self.client.get(reverse("restaurant_kitchen:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "restaurant_kitchen/index.html")
        self.assertIn("num_cooks", response.context)
        self.assertIn("num_dish_types", response.context)
        self.assertIn("num_visits", response.context)

    def test_index_view_increment_visits(self):
        session = self.client.session
        session["num_visits"] = 5
        session.save()
        response = self.client.get(reverse("restaurant_kitchen:index"))
        self.assertEqual(response.context["num_visits"], 6)
