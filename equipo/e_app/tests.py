from django.test import TestCase
from django.urls import reverse

class DatingRequestViewTests(TestCase):
    def test_dating_request_page_status_code(self):
        response = self.client.get(reverse('dating_request'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'dating_request.html')

    def test_dating_request_contains_key_elements(self):
        response = self.client.get(reverse('dating_request'))
        content = response.content.decode('utf-8')
        
        # Check core interactive elements
        self.assertIn('eye-companion', content)
        self.assertIn('yes-spotlight', content)
        self.assertIn('no-btn', content)
        self.assertIn('user-name-input', content)
        self.assertIn('questions-container', content)
        self.assertIn('copy-summary-btn', content)
        self.assertIn('wa-link', content)
        self.assertIn('email-link', content)
        self.assertIn('romanticMessagesPool', content)
