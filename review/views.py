from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from review.serializers import TokenSerializer, CompanySerializer, ReviewSerializer

from review.models import Company
from review.models import Review

class UserViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows users to be viewed or edited.
    """
    queryset = Token.objects.all().order_by('key')
    serializer_class = TokenSerializer
    http_method_names = ['get']


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
