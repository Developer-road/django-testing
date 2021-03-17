from django.test import TestCase, SimpleTestCase

from django.urls import reverse, resolve

from budget.views import *

# Create your tests here.

# Url patterns
# urlpatterns = [
#     path('', views.project_list, name='list'),
#     path('add/', views.ProjectCreateView.as_view(), name='add'),
#     path('<slug:project_slug>/', views.project_detail, name='detail')
# ]


class TestUrls(SimpleTestCase):
    
    def test_list_url_resolves(self):
        url = reverse("list")

        # Asserts that the home url points to the view function project list
        self.assertEquals(resolve(url).func, project_list)

    def test_create_project_url_resolves(self):
        url = reverse("add")

        # Asserts that the add url points to the CBV ProjectCreateView 
        self.assertEquals(resolve(url).func.view_class, ProjectCreateView)
    
    def test_project_detail_url_resolves(self):
        url = reverse("detail", args=["some-slug"])

        # Asserts that the detail url points to the function project_detail 
        self.assertEquals(resolve(url).func, project_detail)
