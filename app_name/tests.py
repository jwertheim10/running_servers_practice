from django.test import TestCase
from django.urls import reverse

class TestSummingMultiples(TestCase):
    def test_summing_multiples_valid_case(self):
        # Simulate a GET request with query parameters num1=2 and num2=16
        response = self.client.get(reverse('sum_multiples'), {'num1': 2, 'num2': 16})
        # We expect the response content to contain the correct sum message
        expected_result = "The sum of all multiples of 2 below 16 is 72"
        self.assertContains(response, expected_result)

    def test_summing_multiples_invalid_case(self):
        response = self.client.get(reverse('sum_multiples'), {'num1': 10, 'num2': 3})
        # We expect the response content to contain the error message
        expected_result = 'Your second number must be greater than or equal to your first number'
        self.assertContains(response, expected_result)
