from django.contrib import admin

from review.models import Company
from review.models import Review

admin.site.register(Company)
admin.site.register(Review)