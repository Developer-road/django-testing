from django.test import TestCase

from django.urls import reverse

from budget.models import *

import json


# We should test every possible scenario.
# That includes all the available HTTP methods in our views

class TestViews(TestCase):

    # At first we have a setUp function.
    # This will create some models, views or urls to work with

    # That function will contain all the code, and the test functions will contain only the assertions

    def setUp(self):
        self.list_url = reverse('list')

        self.project1 = Project.objects.create(
            name="project1",
            budget=10000)

        self.category1 = Category.objects.create(
            name="category1", project=self.project1)

        self.category2 = Category.objects.create(
            name="category2", project=self.project1)

        self.expense1 = Expense.objects.create(project=self.project1,
                                               amount=2000,
                                               title="Expense number 1",
                                               category=self.category2)

        self.detail_url = reverse('detail', args=["project1"])

        self.create_url = reverse('add')

    def test_project_list_GET(self):

        # A Http Response
        response = self.client.get(self.list_url)

        # In get views, we need to:
        # assert the status code = 200
        # assert the template used

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "budget/project-list.html")

    def test_project_detail_GET(self):

        response = self.client.get(self.detail_url)

        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "budget/project-detail.html")

    def test_project_detail_POST_new_expense(self):
        """
        Adds a new expense according to the view
        """

        form = {}

        form["title"] = "test expense"

        form["amount"] = 1200

        form["category"] = "category1"

        response = self.client.post(self.detail_url, form)

        # Asserts that it redirects to the same project page
        self.assertEquals(response.status_code, 302)

        # Query the testing database, and gets the title of the first expense (related name) of the project one
        self.assertEquals(self.project1.expenses.first().title, "Expense number 1")

    def test_project_detail_POST_no_data(self):

        form = {}

        # No data is passed

        response = self.client.post(self.detail_url, form)

        # Asserts that it redirects to the same project page
        self.assertEquals(response.status_code, 302)

        self.assertEquals(self.project1.expenses.count(), 1)


    def test_project_detail_DELETE_expenses(self):

        form = {"id": self.expense1.id}

        response = self.client.delete(self.detail_url, json.dumps(form))

        self.assertEquals(response.status_code, 204)

        # We just delete the expense, so there won't be any expenses
        self.assertEquals(self.project1.expenses.count(), 0)

    def test_project_detail_DELETE_no_id(self):

        # Empty dictionary
        form = {}

        response = self.client.delete(self.detail_url, json.dumps(form))

        self.assertEquals(response.status_code, 404)

        # We didn't pass id to the form so it will still one expense only
        self.assertEquals(self.project1.expenses.count(), 1)

    def test_project_create_view_POST(self):
        
        create_form = {
            "name": "project2",
            "budget": 20000,
            "categoriesString": "new_category,other_category"
        }


        response = self.client.post(self.create_url, create_form)
        
        project_2 = Project.objects.get(name="project2")

        project_2_categories = Category.objects.filter(project=project_2)

        first_category = Category.objects.get(id=3)
        second_category = Category.objects.get(id=4)
    


        self.assertEquals(response.status_code, 302)


        self.assertEquals(project_2.name, "project2")


        # Categories created

        self.assertEquals(project_2_categories.count(), 2)

        self.assertEquals(first_category.name, "new_category")
        
        self.assertEquals(second_category.name, "other_category")


        self.assertEquals(Project.objects.count(), 2)

        self.assertEquals(Category.objects.count(), 4)