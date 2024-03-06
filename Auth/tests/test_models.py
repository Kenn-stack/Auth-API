from django.test import TestCase

from Auth.models import User

from rest_framework.test import APIClient


# Create your tests here.

class ModelTestCase(TestCase):

    def test_user_can_be_created(self):
        user = User.objects.create(email='agwuekene@yahoo.com', password='relat1v1t1')
        user_result = User.objects.last()  #Gets the last entry
        self.assertEqual(user_result.email, 'agwuekene@yahoo.com')

    def test_user_can_be_updated(self):
        user = User.objects.create(email='agwuekene@yahoo.com', password='relat1v1t1')
        user_update = User.objects.filter(email='agwuekene@yahoo.com').update(is_staff=True)  #Gets the last entry
        user_result = User.objects.last()  #Gets the last entry
        self.assertTrue(user_result.is_staff)



class ViewTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        
    
    def test_create_view(self):
        test = self.client.post('users/', {"email": "agwuekene@yahoo.com", "password": "relat1v1t1"}, content_type="json")
        self.assertEqual(test.status_code, 201)
        


