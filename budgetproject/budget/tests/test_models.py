from django.test import TestCase

from budget.models import *

"""
We have to test Model, creation, it's method and properties.
"""

class TestModels(TestCase):

    def setUp(self):
        self.project1 = Project.objects.create(
            name="My project 1",
            budget=10000
        ) 

        self.project_space = Project.objects.create(
            name="Test   Spaces testing  ",
            budget=20000
        )
    
        self.category1 = Category.objects.create(
            name="category1",
            project=self.project1
        )


    def test_project_assigned_slug_on_creation(self):
        self.assertEquals(self.project1.slug, "my-project-1")
    
    def test_project_assigned_slug_strange_spaces(self):

        self.assertEquals(self.project_space.slug, "test-spaces-testing")

    def test_budget_left_property(self):

        category_expenses = Category.objects.create(
            name="A category xd",
            project=self.project1
        )
        
        Expense.objects.create(
            project=self.project1,
            title="expense 1",
            amount=3000,
            category=category_expenses
        )
        
        Expense.objects.create(
            project=self.project1,
            title="expense 2",
            amount=2000,
            category=category_expenses,
        )


        self.assertEquals(self.project1.budget_left, 5000)
    
    def test_project_total_transaction(self):
        
        transaction_project = Project.objects.create(
            name="Daniel's project",
            budget=20000
        )
        
        category_expenses = Category.objects.create(
            name="A category xd",
            project=self.project1
        )
        
        Expense.objects.create(
            project=self.project1,
            title="expense 1",
            amount=3000,
            category=category_expenses
        )
        
        Expense.objects.create(
            project=transaction_project,
            title="expense 2",
            amount=2000,
            category=category_expenses,
        )

        self.assertEquals(self.project1.total_transactions, 1)
        self.assertEquals(transaction_project.total_transactions, 1)
