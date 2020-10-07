from django.urls import path
from django.urls import include
from ems_app.views import UserRegister, UserLogin, AddEnquiry

urlpatterns = [
    path('register', UserRegister.as_view(), name='register'),
    path('login', UserLogin.as_view(), name='login'),
    path('add-enquiry/<int:pk>', AddEnquiry.as_view(), name='add-enquiry'),
]
