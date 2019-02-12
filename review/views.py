from django.contrib.auth.models import User
from rest_framework import viewsets
from review.serializers import UserSerializer, CompanySerializer, ReviewSerializer

from review.models import Company
from review.models import Review

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = User.objects.all().order_by('username')
    serializer_class = UserSerializer

class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows companies to be viewed or edited.
    """
    queryset = Company.objects.all().order_by('name')
    serializer_class = CompanySerializer

class ReviewViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows reviews to be viewed or edited.
    """
    queryset = Review.objects.all().order_by('submission_date')
    serializer_class = ReviewSerializer
