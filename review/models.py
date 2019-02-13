from django.db import models
from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token

class Company(models.Model):
    '''
    Model responsible to keep company informations
    '''
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Review(models.Model):
    '''
    Model responsible to keep review informations
    '''
    RATING_OPTIONS = ((1, '1 star'), (2, '2 stars'), (3, '3 stars'),
                      (4, '4 stars'), (5, '5 stars'))

    rating = models.IntegerField(choices=RATING_OPTIONS)
    title = models.CharField(max_length=64)
    summary = models.CharField(max_length=100000)
    ip_address = models.CharField(max_length=45)  #Allow IPV6 values
    submission_date = models.DateTimeField('date of submission', auto_now_add=True)
    #References
    company = models.ForeignKey(Company, related_name='reviews', on_delete=models.PROTECT)
    reviewer = models.ForeignKey(Token, related_name='reviews', on_delete=models.PROTECT)

