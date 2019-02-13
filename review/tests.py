import pytest
from django.test import TestCase
from django.test import Client
from django.test.client import RequestFactory
from django.urls import include, path, reverse
from django.db.utils import IntegrityError
from django.contrib.auth.models import User
from django.contrib.admin.sites import AdminSite
from django.db.models import Count

from rest_framework.test import APITestCase, URLPatternsTestCase
from rest_framework import status

from review.admin import ReviewAdmin
from review.models import Company
from review.models import Review
from rest_framework.authtoken.models import Token


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
                reviewer = Token.objects.create(user=User.objects.create_user(username='User1'))
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
                reviewer = Token.objects.create(user=User.objects.create_user(username='User1'))
            )

    def test_is_not_possible_create_without_reviwer(self):
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
        reviewer_1 = Token.objects.create(user=User.objects.create_user(username='User1'))
        reviewer_2 = Token.objects.create(user=User.objects.create_user(username='User2'))
        
        r1 = Review.objects.create(
            rating = 1,
            title = 'My test review 1',
            summary = 'This is my test review with summary',
            ip_address = '192.168.0.1',
            company = company,
            reviewer = reviewer_1
        )

        r2 = Review.objects.create(
            rating = 2,
            title = 'My test review 2',
            summary = 'This is my test review with summary',
            ip_address = '192.168.0.1',
            company = company,
            reviewer = reviewer_1
        )        

        r3 = Review.objects.create(
            rating = 3,
            title = 'My test review 3',
            summary = 'This is my test review with summary',
            ip_address = '192.168.0.1',
            company = company,
            reviewer = reviewer_2
        )

        self.assertEqual(Review.objects.filter(reviewer=reviewer_1).count(), 2)
        self.assertEqual(Review.objects.filter(reviewer=reviewer_2).count(), 1)


class CompanyApiTests(APITestCase):

    def setUp(self):
        self.superuser1 = User.objects.create_superuser('john', 'john@snow.com', 'localpass1')
        self.superuser2 = User.objects.create_superuser('drika', 'drika@borne.com', 'localpass2')
        self.token1 = Token.objects.create(user=self.superuser1)
        self.client.login(username='john', password='localpass1')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token1.key)

    
    def test_can_get_all_companies(self):
        '''
        Ensure we can get all companies.
        '''

        Company.objects.create(name='test', description='test description')

        response = self.client.get('/company/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

    def test_is_possible_create_review_for_a_new_company(self):
        '''
        Ensure we can create a review with a new user
        '''
        response = self.client.post('/review/', format='json', data=
            {
                "rating": 1,
                "title": "asdf",
                "summary": "asdf",
                "company": {
                    "name": "asdf",
                    "description": "asdf"
                }
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)       

    def test_is_possible_create_two_reviews_for_the_same_company(self):
        '''
        Ensure we can create a review with the same company
        '''
        response = self.client.post('/review/', format='json', data=
            {
                "rating": 1,
                "title": "asdf",
                "summary": "asdf",
                "company": {
                    "name": "asdf",
                    "description": "asdf"
                }
            })
        response = self.client.post('/review/', format='json', data=
            {
                "rating": 2,
                "title": "asdf - asdf",
                "summary": "asdf - asdf",
                "company": {
                    "name": "asdf",
                    "description": "asdf"
                }
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_is_possible_separate_reviews_from_users(self):
        '''
        Ensure we can create a review for different users
        '''
        response = self.client.post('/review/', format='json', data=
            {
                "rating": 1,
                "title": "asdf",
                "summary": "asdf",
                "company": {
                    "name": "asdf",
                    "description": "asdf"
                }
            })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get('/review/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.token2 = Token.objects.create(user=self.superuser2)
        self.client.login(username='drika', password='localpass2')
        self.client.credentials(HTTP_AUTHORIZATION='Token ' + self.token2.key)
        
        response = self.client.post('/review/', format='json', data=
            {
                "rating": 2,
                "title": "asdf - asdf",
                "summary": "asdf - asdf",
                "company": {
                    "name": "asdf",
                    "description": "asdf"
                }
            })
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        response = self.client.get('/review/', format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)

        self.assertEqual(Review.objects.filter(reviewer=self.token1).count(), 1)
        self.assertEqual(Review.objects.filter(reviewer=self.token2).count(), 1)
        self.assertEqual(Review.objects.all().count(), 2)

    def test_is_not_possible_save_invalid_data_without_title(self):
        '''
        Ensure we can create a review for different users
        '''
        response = self.client.post('/review/', format='json', data=
            {
                "rating": 1,
                "summary": "asdf",
                "company": {
                    "name": "asdf",
                    "description": "asdf"
                }
            })
        self.assertEqual(response.status_code, status.HTTP_500_INTERNAL_SERVER_ERROR)

    
    def test_if_can_save_the_ip_from_requests(self):
        '''
        Ensure we can save the review with the IP address 
        '''
        response = self.client.post('/review/', format='json', data=
            {
                "rating": 1,
                "title": "asdf",
                "summary": "asdf",
                "company": {
                    "name": "asdf",
                    "description": "asdf"
                }
            })

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        review = Review.objects.filter(reviewer=self.token1).first()
        self.assertEqual(review.ip_address, '127.0.0.1')



class ReviewAdminModelTest(TestCase):
    
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        
    def test_if_filter_url_by_logged_user(self):

        normaluser = User.objects.create_user(
            username='john', email='john@snow.com', password='localpass1')
        token = Token.objects.create(user=normaluser)

        # Create an instance of a GET request.
        request = self.factory.get('/admin/review/review/')
        request.user = normaluser

        adm_rev = ReviewAdmin(Review, AdminSite())
        adm_rev.get_queryset(request)

        query = str(adm_rev.get_queryset(request).query)

        self.assertEqual(query.split('WHERE')[1].strip(), f'"review_review"."reviewer_id" = {token.key}')

    def test_if_filter_url_by_logged_superuser(self):

        normaluser = User.objects.create_superuser(
            username='john', email='john@snow.com', password='localpass1')
        token = Token.objects.create(user=normaluser)

        # Create an instance of a GET request.
        request = self.factory.get('/admin/review/review/')
        request.user = normaluser

        adm_rev = ReviewAdmin(Review, AdminSite())
        adm_rev.get_queryset(request)

        query = str(adm_rev.get_queryset(request).query)

        self.assertTrue('WHERE' not in query)





