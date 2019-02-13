from rest_framework.authtoken.models import Token
from rest_framework import viewsets
from rest_framework.response import Response

from review.serializers import CompanySerializer, ReviewSerializer
from review.models import Company
from review.models import Review

class CompanyViewSet(viewsets.ModelViewSet):
    """
    API endpoint that allows companies to be viewed or edited.
    """
    queryset = Company.objects.all().order_by('name')
    serializer_class = CompanySerializer
    http_method_names = ['get']
    
class ReviewViewSet(viewsets.ViewSet):
    """
    API endpoint that allows reviews to be viewed or edited.
    """
    http_method_names = ['get', 'post']

    def list(self, request):
        reviwer = Token.objects.get(user=request.user)
        queryset = Review.objects.filter(reviewer=reviwer).order_by('submission_date')
        serializer = ReviewSerializer(queryset, many=True)
        return Response(serializer.data)

    def create(self, request):
        request_data = request.data
        request_data['reviewer'] = {'user': {'username': request.user.username, 'email': request.user.email}, 'key': '-'}
        # GET request IP
        request_data['ip_address'] = request.META.get('HTTP_X_FORWARDED_FOR', request.META.get('REMOTE_ADDR')).split(',')[0]
            
        serializer = ReviewSerializer(data=request_data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=500)
        serializer.save()
        return Response(serializer.data, status=201)
        