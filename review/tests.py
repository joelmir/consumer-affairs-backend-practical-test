import pytest
from django.test import TestCase
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.db.models import Count

from review.models import Company
from review.models import Review


class CompanyModelTest(TestCase):

    def test_is_posible_create_with_valid_parameters(self):
        c = Company.objects.create(name='Company 1', description='This is a test company')
        self.assertEqual(str(c), c.name)

    def test_is_not_posible_create_with_duplicated_name(self):
        c1 = Company.objects.create(name='Company 1', description='This is a test company')
        with pytest.raises(IntegrityError, match="UNIQUE constraint failed: review_company.name"):
            c2 = Company.objects.create(name='Company 1', description='This is a test company')


class ReviewModelTest(TestCase):

    def test_is_possible_create_with_valid_parameters(self):
        company = Company.objects.create(name='Company 1', description='This is a test company')

        r = Review.objects.create(
                rating = 1,
                title = 'My test review',
                summary = 'This is my test review with summary',
                ip_address = '192.168.0.1',
                company = company,
                reviewer = User.objects.create_user(username='User1')
            )
        self.assertEqual(r.title, 'My test review')
        self.assertEqual(r.company, company)

    def test_is_not_possible_create_without_company(self):
        with pytest.raises(IntegrityError, match="NOT NULL constraint failed: review_review.company_id"):
            Review.objects.create(
                rating = 1,
                title = 'My test review',
                summary = 'This is my test review with summary',
                ip_address = '192.168.0.1',
                reviewer = User.objects.create_user(username='User1')
            )

    def test_is_not_possible_create_without_user(self):
        company = Company.objects.create(name='Company 1', description='This is a test company')

        with pytest.raises(IntegrityError, match="NOT NULL constraint failed: review_review.reviewer_id"):
            Review.objects.create(
                rating = 1,
                title = 'My test review',
                summary = 'This is my test review with summary',
                ip_address = '192.168.0.1',
                company = company
            )

    def test_if_can_get_all_reviews_from_one_user(self):
        company = Company.objects.create(name='Company 1', description='This is a test company')
        user1 = User.objects.create_user(username='User1')
        user2 = User.objects.create_user(username='User2')
        
        r1 = Review.objects.create(
            rating = 1,
            title = 'My test review 1',
            summary = 'This is my test review with summary',
            ip_address = '192.168.0.1',
            company = company,
            reviewer = user1
        )

        r2 = Review.objects.create(
            rating = 2,
            title = 'My test review 2',
            summary = 'This is my test review with summary',
            ip_address = '192.168.0.1',
            company = company,
            reviewer = user1
        )        

        r3 = Review.objects.create(
            rating = 3,
            title = 'My test review 3',
            summary = 'This is my test review with summary',
            ip_address = '192.168.0.1',
            company = company,
            reviewer = user2
        )

        self.assertEqual(Review.objects.filter(reviewer=user1).count(), 2)
        self.assertEqual(Review.objects.filter(reviewer=user2).count(), 1)

