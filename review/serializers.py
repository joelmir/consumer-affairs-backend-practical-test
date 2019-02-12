from django.contrib.auth.models import User

from rest_framework.authtoken.models import Token
from rest_framework import serializers

from review.models import Company
from review.models import Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class TokenSerializer(serializers.ModelSerializer):
    user = UserSerializer()
    key = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Token
        fields = ('user', 'key')

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'description')

class CompanyReviewSerializer(serializers.Serializer):
    name = serializers.CharField(max_length=200)
    description = serializers.CharField(max_length=1000)

class UserReviewSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=200)
    email = serializers.CharField(max_length=1000)

class TokenReviewSerializer(serializers.Serializer):
    key = serializers.StringRelatedField(read_only=True)
    user = UserReviewSerializer()

class ReviewSerializer(serializers.ModelSerializer):
    company = CompanyReviewSerializer()
    reviewer = TokenReviewSerializer()
    ip_address = serializers.StringRelatedField(read_only=True)
    
    class Meta:
        model = Review
        fields = ('rating', 'title', 'summary', 'ip_address', 'submission_date', 'company', 'reviewer')

    def validate_company(self, validated_company):
        return Company.objects.get_or_create(
            name=validated_company['name'], 
            defaults={'description': validated_company['description']})[0]

    def validate_reviewer(self, validated_reviewer):
        user = User.objects.get_or_create(
            username=validated_reviewer['user']['username'], 
            email=validated_reviewer['user']['email'])[0]
        return Token.objects.get_or_create(user=user)[0]

    def create(self, validated_data):
        review = Review.objects.create(**validated_data)
        return review