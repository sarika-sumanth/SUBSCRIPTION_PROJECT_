# app1/models.py or app2/models.py (or any other app where CustomUser is defined)
from django.db import models
from django.contrib.auth.models import Permission,Group
from django.contrib.auth.models import AbstractUser

class CustomUser(AbstractUser):
    groups = models.ManyToManyField(Group, related_name='custom_users')


    # Add a related_name argument to the user_permissions field.
    user_permissions = models.ManyToManyField(
        Permission,
        blank=True,
        related_name="customuser_permissions",
        verbose_name="user permissions",
        help_text="Specific permissions for this user.",
    )

class Subscription(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    # Other fields for the Subscription model


# models.py



class Payment(models.Model):
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    currency = models.CharField(max_length=3)
    payment_intent_id = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)



class BillingPlan(models.Model):
    name = models.CharField(max_length=100)
    monthly_price = models.DecimalField(max_digits=6, decimal_places=2)
    yearly_price = models.DecimalField(max_digits=6, decimal_places=2)
    video_quality = models.CharField(max_length=100)
    resolution = models.CharField(max_length=100)
    devices = models.CharField(max_length=100)
    active_screens = models.PositiveIntegerField()

    def __str__(self):
        return self.name
