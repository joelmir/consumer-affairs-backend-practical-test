from django.contrib import admin

from rest_framework.authtoken.models import Token
from review.models import Company
from review.models import Review

class ReviewAdmin(admin.ModelAdmin): 
    def get_queryset(self, request): 
        qs = super(ReviewAdmin, self).get_queryset(request) 
        if not request.user.is_superuser:
            return qs.filter(reviewer=Token.objects.get(user=request.user))
        else:
            return qs


admin.site.register(Company)
admin.site.register(Review, ReviewAdmin)