from django.db import models

# Create your models here.
class ActivityTracking(models.Model):
    is_active = models.BooleanField(default=False)
    is_delete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class Users(ActivityTracking):
    full_name = models.CharField(max_length=50, null=False, blank=False)
    email = models.EmailField(unique=True)
    mobile = models.BigIntegerField(null=False, blank=False)
    password = models.CharField(max_length=50, blank=False, null=False)

    def __str__(self):
        return self.email

class Enquiry(ActivityTracking):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    enquiry_subject = models.CharField(max_length=500, null=True, blank=True)
    enquiry_description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.enquiry_subject
