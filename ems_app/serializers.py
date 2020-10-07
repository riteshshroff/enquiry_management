from rest_framework import serializers
from ems_app.models import Users, Enquiry

class UserRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Users
        fields = ['id', 'full_name', 'email', 'mobile', 'password']

class AddEnquirySerializer(serializers.ModelSerializer):
    class Meta:
        model = Enquiry
        fields = ['id', 'user_id', 'enquiry_subject', 'enquiry_description']
