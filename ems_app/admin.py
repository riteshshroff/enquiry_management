from django.contrib import admin
from ems_app.models import Users, Enquiry

class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'full_name', 'email', 'mobile', 'password', 'created_at', 'updated_at')

class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'enquiry_subject', 'enquiry_description')
admin.site.register(Users, UserAdmin)
admin.site.register(Enquiry, EnquiryAdmin)
