from django.shortcuts import render
from ems_app.models import Users, Enquiry
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status, permissions
from ems_app.serializers import UserRegisterSerializer, AddEnquirySerializer
from rest_framework.response import Response
from EMS_Project.settings import EMAIL_HOST_USER
from django.core.mail import EmailMultiAlternatives
import re
import json
import datetime

# User Register API
class UserRegister(APIView):
    serializer_class = UserRegisterSerializer
    def post(self, request, *args, **kwargs):        
        data = request.data        
        name = data['full_name']
        email = data['email']
        mobile = data['mobile']
        password = data['password']
        print(data, name, email, mobile, password)
        if not name:
            return Response({
                "data":[],
                "status":False,
                "code":status.HTTP_404_NOT_FOUND,
                "message":"Name is required."                
            }, status = status.HTTP_404_NOT_FOUND)
        if not email:
            return Response({
                "data":[],
                "status":False,
                "code":status.HTTP_404_NOT_FOUND,
                "message":"Email is required."                
            }, status = status.HTTP_404_NOT_FOUND)
        if not mobile:
            return Response({
                "data":[],
                "status":False,
                "code":status.HTTP_404_NOT_FOUND,
                "message":"Mobile is required."                
            }, status = status.HTTP_404_NOT_FOUND)
        if not password:
            return Response({
                "data":[],
                "status":False,
                "code":status.HTTP_404_NOT_FOUND,
                "message":"Password is required."                
            }, status = status.HTTP_404_NOT_FOUND)        
        if not (name and email and mobile and password):
            return Response({
                "data":[],
                "status":False,
                "code":status.HTTP_404_NOT_FOUND,
                "message":"All fields are required."
            })
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return Response({
                "data":[],
                "status":False,                
                "code":status.HTTP_404_NOT_FOUND,
                "message":"Check your email and please follow this: 'example12@xyz11.com' format."
            }, status=status.HTTP_404_NOT_FOUND)
        if not re.match(r'^\+?1?\d{10,14}$', mobile):
            return Response({
                "data":[],
                "status":False,
                "code":status.HTTP_200_OK,                
                "message":"Check your mobile number and please follow this: '+975455454545' format."
            }, status=status.HTTP_200_OK)         
        user = Users.objects.filter(email=email).distinct()
        if user:            
            return Response({
                "data":[],
                "status":False,
                "code":status.HTTP_404_NOT_FOUND,                    
                "message":"User is already exist with this email-id."
            }, status=status.HTTP_404_NOT_FOUND)
        else:
            serializer = UserRegisterSerializer(data=data)                                             
            if serializer.is_valid():                                
                try:                                                                                               
                    # Start Email Code...                   
                    subject = "Hi " + name + ". | This is an information email from Enquiry Management System."
                    from_email = EMAIL_HOST_USER
                    to = email         
                    text_content = "Hi "+ name + " you are successfully register in EMS_App."
                    html_content = '<h2>You are successfully register on EMS App.</h2>\n<h5 style="color:blue">' + 'Your registered Email: ' + email + '</h5>'
                    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
                    msg.attach_alternative(html_content, "text/html")
                    msg.send()    
                    user_data = Users(full_name=name,mobile=mobile,email=email,password=password).save()    
                    details = Users.objects.get(email=email)                                                                
                    ids = details.id
                    serializer.validated_data['id'] = ids                                                   
                    return Response({
                        "data":serializer.data,                        
                        "status":True,                        
                        "code":status.HTTP_200_OK,
                        "message":"User registered.",
                    }, status= status.HTTP_200_OK)
                except:
                    return Response({
                        "data":[],                        
                        "status":False,                        
                        "code":status.HTTP_200_OK,
                        "message":"Email does not exist.",
                    }, status= status.HTTP_200_OK)
            else:
                return Response({
                    "data":serializer.errors,
                    "status":False,
                    "code":status.HTTP_404_NOT_FOUND,
                    "message":"Serializer error.",
                }, status= status.HTTP_404_NOT_FOUND)

# User Login API
class UserLogin(APIView):    
    def post(self, request, format=None):        
        data = request.data
        email = data['email']        
        password = data['password']            
        if not email:
            return Response({
                "data":[],
                "status":False,
                "code":status.HTTP_404_NOT_FOUND,
                "message":"Email is required."
            }, status= status.HTTP_404_NOT_FOUND)
        if not re.match(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
            return Response({
                "data":[],
                "status":False,                
                "code":status.HTTP_404_NOT_FOUND,
                "message":"Check your email and please follow this: 'example12@xyz11.com' format."
            }, status=status.HTTP_404_NOT_FOUND)                           
        if not password:
            return Response({
                "data":[],
                "status":False,
                "code":status.HTTP_404_NOT_FOUND,
                "message":"Password is required."
            }, status= status.HTTP_404_NOT_FOUND)
        if not (email and password):
            return Response({
                "data":[],
                "status":False,
                "code":status.HTTP_404_NOT_FOUND,
                "message":"Both fields required."
            }, status= status.HTTP_404_NOT_FOUND)
        try:        
            user = Users.objects.get(email=email)            
            check_pass = user.password
            if check_pass == password:
                serializer = UserRegisterSerializer(data=data)
                if serializer.is_valid:
                    return Response({   
                        # "data":serializer.data,
                        "status":True,                        
                        "code":status.HTTP_200_OK,
                        "message":"User login successfully.",
                    }, status= status.HTTP_200_OK)
                else:
                    return Response({
                        "data":[],
                        "status":False,
                        "code":status.HTTP_404_NOT_FOUND,
                        "message":"Serializer error.",
                    }, status= status.HTTP_404_NOT_FOUND)
            else:
                return Response({
                        "data":[],                        
                        "status":False,                        
                        "code":status.HTTP_404_NOT_FOUND,
                        "message":"Invalid Password.",
                    }, status= status.HTTP_404_NOT_FOUND)
        except:                
            return Response({
                "data":[],                        
                "status":False,                        
                "code":status.HTTP_404_NOT_FOUND,
                "message":"Email id does not exist.",
            }, status= status.HTTP_404_NOT_FOUND)

# User Enquiry API
class AddEnquiry(APIView):    
    def post(self, request, pk, *args, **kwargs):
        data = request.data
        subject = data['subject']
        enquiry = data['enquiry']
        if not subject:
            return Response({
                "data":[],
                "status":False,
                "code":status.HTTP_404_NOT_FOUND,
                "message":"Enquiry subject is required."                
            }, status = status.HTTP_404_NOT_FOUND)
        if not enquiry:
            return Response({
                "data":[],
                "status":False,
                "code":status.HTTP_404_NOT_FOUND,
                "message":"Enquiry description is required."                
            }, status = status.HTTP_404_NOT_FOUND)
        if not (subject and enquiry):
            return Response({
                "data":[],
                "status":False,
                "code":status.HTTP_404_NOT_FOUND,
                "message":"Both fields are required."                
            }, status = status.HTTP_404_NOT_FOUND)
        try:
            user = Users.objects.get(pk=pk)   
            details = Enquiry.objects.filter(enquiry_subject=subject)
            serializers = AddEnquirySerializer(data=data)        
            if serializers.is_valid():                   
                obj = Enquiry()
                obj.user = user
                obj.enquiry_subject = subject
                obj.enquiry_description = enquiry
                obj.save()
                serializers.validated_data['id'] = obj.id
                serializers.validated_data['enquiry_subject'] = subject
                serializers.validated_data['enquiry_description'] = enquiry
                return Response({
                    "data":serializers.data,    
                    "status":True,
                    "code":status.HTTP_200_OK,      
                    "message":"Enquiry successed."                
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    "data":[],
                    "status":False,
                    "code":status.HTTP_400_BAD_REQUEST,
                    "message":"Serializer Error."                
                }, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({
                "data":[],
                "status":False,
                "code":status.HTTP_404_NOT_FOUND,
                "message":"User does not exist."                
            }, status=status.HTTP_404_NOT_FOUND)             








