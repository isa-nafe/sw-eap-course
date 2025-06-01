from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from .models import UserPayment # Assuming UserPayment is needed for some tests

class CourseViewTests(TestCase):

    def setUp(self):
        # Create a user for testing login-required views
        self.user = User.objects.create_user(username='testuser', password='password123')
        # UserPayment profile is created by signals
        self.client = Client()

    def test_dashboard_view_anonymous(self):
        # Test that anonymous users are redirected from dashboard (due to @login_required)
        response = self.client.get(reverse('course:dashboard'))
        self.assertEqual(response.status_code, 302) # Should redirect to login
        self.assertIn(reverse('course:login'), response.url)

    def test_dashboard_view_authenticated(self):
        # Test that authenticated users can access the dashboard
        self.client.login(username='testuser', password='password123')
        response = self.client.get(reverse('course:dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Welcome, testuser!")

    def test_registration_page_loads(self):
        response = self.client.get(reverse('course:register'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Register")

    def test_login_page_loads(self):
        response = self.client.get(reverse('course:login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Login")

    # Example of a test that might require a paid user (more complex setup)
    # def test_materials_list_for_paid_user(self):
    #     self.client.login(username='testuser', password='password123')
    #     user_payment = UserPayment.objects.get(user=self.user)
    #     user_payment.has_paid_for_course = True
    #     user_payment.save()
    #     response = self.client.get(reverse('course:course_materials_list'))
    #     self.assertEqual(response.status_code, 200)
    #     # Add more assertions here, e.g., checking for specific material content
    #     # or absence of "payment required" message.


    # To run these tests: python manage.py test course
