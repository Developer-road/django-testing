from django.test import SimpleTestCase

from budget.forms import ExpenseForm

class TestForms(SimpleTestCase):

    def test_form_with_correct_data(self):
        form = {
            "title": "Correct data form",
            "amount": 1000,
            "category": "correct category",
        }

        correct_form = ExpenseForm(data=form)

        self.assertTrue(correct_form.is_valid())

    def test_form_invalid_string(self):
        invalid_title = "This is a long title" + "e" * 100

        form = {
            "title": invalid_title,
            "amount": 1000,
            "category": "correct category",
        }

        invalid_form = ExpenseForm(data=form)

        self.assertFalse(invalid_form.is_valid())

        self.assertEquals(len(invalid_form.errors), 1)
        
    def test_form_invalid_no_data(self):

        form = ExpenseForm(data={})

        self.assertFalse(form.is_valid())

        self.assertEquals(len(form.errors), 3)
    