from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework import serializers

from review.models import Company
from review.models import Review

class CompanySerializer(serializers.ModelSerializer):
    '''
    Company model serializer
    '''
    class Meta:
        model = Company
        fields = ('name', 'description')

class UserSerializer(serializers.Serializer):
    '''
    Custon User model serializer
    '''
    username = serializers.CharField(max_length=150)
    email = serializers.CharField(max_length=150, allow_blank=True)

class TokenSerializer(serializers.Serializer):
    '''
    Custon Token model serializer
    '''
    user = UserSerializer()
    key = serializers.CharField(max_length=200)
    
class CompanyReviewSerializer(serializers.Serializer):
    '''
    Custon Company model serializer
    '''
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000)

class ReviewSerializer(serializers.ModelSerializer):
    '''
    Review model serializer
    '''

    company = CompanyReviewSerializer()
    reviewer = TokenSerializer()
    
    class Meta:
        model = Review
        fields = ('rating', 'title', 'summary', 'ip_address', 'submission_date', 'company', 'reviewer')

    def validate_company(self, validated_company):
        '''
        Load or Create company model using the request data 
        '''
        return Company.objects.get_or_create(
            name=validated_company['name'], 
            defaults={'description': validated_company['description']})[0]

    def validate_reviewer(self, validated_reviewer):
        '''
        Load Reviewer (Token) model using the request data 
        '''
        user = User.objects.get(
            username=validated_reviewer['user']['username'], 
            email=validated_reviewer['user']['email'])
        return Token.objects.get(user=user)
