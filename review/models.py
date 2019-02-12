from django.db import models
from django.contrib.auth.models import User


class Company(models.Model):
    name = models.CharField(max_length=200, unique=True)
    description = models.CharField(max_length=1000)

    def __str__(self):
        return self.name


class Review(models.Model):
    RATING_OPTIONS = ((1, '1 star'), (2, '2 stars'), (3, '3 stars'),
                      (4, '4 stars'), (5, '5 stars'))
    
    rating = models.IntegerField(choices=RATING_OPTIONS)
    title = models.CharField(max_length=64)
    summary = models.CharField(max_length=100000)
    ip_address = models.CharField(max_length=45)  #Allow IPV6 values
    submission_date = models.DateTimeField('date of submission', auto_now_add=True)
    company = models.ForeignKey(Company, on_delete=models.PROTECT)
    reviewer = models.ForeignKey(User, on_delete=models.PROTECT)
