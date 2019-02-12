from django.contrib.auth.models import User, Group
from rest_framework import serializers

from review.models import Company
from review.models import Review

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email')

class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = ('name', 'description')

class ReviewSerializer(serializers.ModelSerializer):
    company = CompanySerializer()
    reviewer = UserSerializer()
    class Meta:
        model = Review
        fields = ('rating', 'title', 'summary', 'ip_address', 'submission_date', 'company', 'reviewer')