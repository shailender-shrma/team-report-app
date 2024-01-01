from testcase.models import User, TestCase
from django.test import TestCase as TC
from django.utils import timezone


class UserTest(TC):
    def test_without_login(self):
        response = self.client.get('/addtestcase/')
        self.assertRedirects(response, '/login/?next=/addtestcase/')

    def test_with_login(self):
        user = User.objects.create_user(username="testuser", password="testpassword")
        login = self.client.login(username='testuser', password='testpassword')
        self.assertTrue(login)
        response = self.client.get('/addtestcase/')
        self.assertTrue(response)
        test = TestCase.objects.create(status='PASS',
                                       test_description="helo",
                                       created_by=user,
                                       comment='hello',
                                       created_at=timezone.now())
        self.assertEqual(response.status_code, 200)
    

    def test_add_testcase(self):
        user=User.objects.create_user(username="testuser",
                                      password="testpassword")
        login=self.client.login(username='testuser', password='testpassword')
        response = self.client.get('/home/')
