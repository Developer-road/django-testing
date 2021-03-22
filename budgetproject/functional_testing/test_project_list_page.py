from selenium import webdriver

from django.urls import reverse

from django.contrib.staticfiles.testing import StaticLiveServerTestCase

from budget.models import Project

import time


class TestProjectListPage(StaticLiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()   

        # export geckodriver="~/.local/bin/geckodriver"

        self.add_project_url = self.live_server_url + reverse("add")
        

    def tearDown(self):
        self.browser.close()
    
    def test_no_projects_text_displayed(self):
        self.browser.get(self.live_server_url)

        # User request the site, and haven't created a project yet

        div = self.browser.find_element_by_class_name("noproject-wrapper")

        text = div.find_element_by_tag_name("h3").text

        self.assertEquals(text, "Sorry, you don't have any projects, yet.")
    
    def test_no_projects_button_redirects(self):

        self.browser.get(self.live_server_url)

        # The users click on the button link of create project


        self.browser.find_element_by_tag_name("a").click()

        self.assertEquals(self.browser.current_url, self.add_project_url)

    def test_user_sees_project_list(self):
        
        # Project created so user doesn't sees alert
        project1 = Project.objects.create(
            name="project1",
            budget=12000
        )

        # User gets the home page
        self.browser.get(self.live_server_url)
    
        # Asserts that the h5 tag contains the text of the project1 name

        self.assertEquals(
            self.browser.find_element_by_tag_name("h5").text,
            project1.name)

        # User clicks in add project button
        self.browser.find_element_by_css_selector("span.bold").click()


        self.assertEquals(
            self.browser.current_url,
            self.add_project_url
        )

    def test_user_redirected_project_detail(self):
        # Project created so user doesn't sees alert
        project1 = Project.objects.create(
            name="project1",
            budget=12000
        )

        # User gets the home page
        self.browser.get(self.live_server_url)

        # User sees and clicks on "Visit" the project
        # Then is redirected to the detail page

        detail_project_url = self.live_server_url + reverse("detail", args=[project1.slug])

        self.browser.find_element_by_link_text('VISIT').click()

        self.assertEquals(
            self.browser.current_url,
            detail_project_url
        )



        

    
