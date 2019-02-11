from django.test import TestCase

from review.models import Company
from review.models import Review

class CompanyModelTest(TestCase):

    def test_is_posible_create_with_valid_parameters(self):
        c = Company(name='Company 1', description='This is a test company')
        self.assertEqual(str(c), c.name)
