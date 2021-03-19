from selenium import webdriver

from django.urls import reverse

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from budget.models import Project


class TestProjectListPage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()    

    def tearDown(self):
        self.browser.close()
    
    def test_no_projects_text_displayed(self):
        self.browser.get(self.live_server_url)

        # User request the site, and haven't created a project yet

        div = self.browser.find_element_by_class_name("noproject-wrapper")

        text = div.find_element_by_tag_name("h3").text

        self.assertEquals(text, "Sorry, you don't have any projects, yet.  ")

        

    
