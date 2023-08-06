# users/admin.py (if your custom user model is in the 'users' app)
from django.contrib import admin
from .models import CustomUser
from .models import BillingPlan

admin.site.register(BillingPlan)
admin.site.register(CustomUser)