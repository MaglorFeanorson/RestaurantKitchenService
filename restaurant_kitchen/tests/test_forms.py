from django.contrib.auth import get_user_model
from django.test import TestCase
from restaurant_kitchen.models import Cook, Dish, DishType
from restaurant_kitchen.forms import (
    CookCreationForm,
    DishForm,
    DishSearchForm,
    CookSearchForm,
    DishTypeSearchForm
)


class FormsTest(TestCase):

    def setUp(self):
        self.cook = get_user_model().objects.create_user(
            username="TestCook",
            password="testpass123",
            first_name="Test",
            last_name="Cook",
            years_of_experience=5
        )
        self.dish_type = DishType.objects.create(
            name="Appetizer"
        )
        self.dish1 = Dish.objects.create(
            name="Dish1",
            description="Description1",
            price=10.00,
            dish_type=self.dish_type
        )
        self.dish2 = Dish.objects.create(
            name="Dish2",
            description="Description2",
            price=20.00,
            dish_type=self.dish_type
        )

    def test_cook_creation_form_is_valid(self):
        form_data = {
            "username": "newcook",
            "password1": "cook12test",
            "password2": "cook12test",
            "first_name": "John",
            "last_name": "Doe",
            "years_of_experience": 3
        }
        form = CookCreationForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "newcook")
        self.assertEqual(form.cleaned_data["years_of_experience"], 3)

    def test_cook_creation_form_invalid_years_of_experience(self):
        form_data = {
            "username": "newcook",
            "password1": "cook12test",
            "password2": "cook12test",
            "first_name": "John",
            "last_name": "Doe",
            "years_of_experience": -1  # Invalid value
        }
        form = CookCreationForm(data=form_data)
        self.assertFalse(form.is_valid())
        self.assertIn("years_of_experience", form.errors)

    def test_dish_form_is_valid(self):
        form_data = {
            "name": "Dish3",
            "description": "Description3",
            "price": 15.00,
            "dish_type": self.dish_type.id,
            "cooks": [self.cook.id]
        }
        form = DishForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Dish3")
        self.assertEqual(form.cleaned_data["description"], "Description3")
        self.assertEqual(form.cleaned_data["price"], 15.00)
        self.assertEqual(form.cleaned_data["dish_type"], self.dish_type)
        self.assertEqual(list(form.cleaned_data["cooks"]), [self.cook])

    def test_dish_search_form_is_valid(self):
        form_data = {"name": "Dish1"}
        form = DishSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Dish1")

    def test_dish_search_form_empty_name_is_valid(self):
        form_data = {"name": ""}
        form = DishSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")

    def test_cook_search_form_is_valid(self):
        form_data = {"username": "TestCook"}
        form = CookSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "TestCook")

    def test_cook_search_form_empty_username_is_valid(self):
        form_data = {"username": ""}
        form = CookSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["username"], "")

    def test_dish_type_search_form_is_valid(self):
        form_data = {"name": "Appetizer"}
        form = DishTypeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "Appetizer")

    def test_dish_type_search_form_empty_name_is_valid(self):
        form_data = {"name": ""}
        form = DishTypeSearchForm(data=form_data)
        self.assertTrue(form.is_valid())
        self.assertEqual(form.cleaned_data["name"], "")
