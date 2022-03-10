from django.shortcuts import render
from rest_framework.generics import GenericAPIView
from .serializers import RegisterSerializer, ProfileSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import Profile
from rest_framework.views import APIView
from django.contrib.auth.hashers import make_password, check_password
from django.contrib.auth import authenticate

from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)

class Register_Users(GenericAPIView, CreateModelMixin):
    queryset= User.objects.all()
    serializer_class= RegisterSerializer

    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        data = {}
        account = ""
        serializer = RegisterSerializer(data=request.data)
        user = User.objects.filter(email=request.data["email"])
        if serializer.is_valid():
            if not user:
                if request.data["password"] == request.data["password2"]: 
                    account = serializer.save()
                else: 
                    return Response({"Status": "Passowords are not the same"})
                if not user:
                    account.is_active = True
                    account.save()
                    token = Token.objects.get_or_create(user=account)[0].key
                    data["message"] = "User registered successfully"
                    data["email"] = account.email
                    data["username"] = account.username
                    data["token"] = token
                    user = User.objects.filter(email=account.email)
                    user = user[0]
                    name = request.data["name"]
                    surname = request.data["surname"]
                    profile = Profile.objects.create(user=user, name=name, surname=surname)
                    profile.save()
                else:
                    return Response({"Status": "This e-mail already exist, try another one"})
            else:
                return Response({"Status": "This e-mail already exist, try another one"})
        else:

            data = serializer.errors

        return Response(data)

class Login_Users(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        Account = User.objects.get(username=request.data["username"])
        password = request.data["password"]
        username = request.data["username"]
        try:
            if authenticate(username=username, password=password):
                token = Token.objects.get_or_create(user=Account)[0].key
                return Response({"token":token, "message":"User logged in"})
            else:
                return Response({"Status":Account.password, "Digitada":password})
        except Account.DoesNotExist:
            return Response({"Status": "User doens't exist"})

# class ProfileView(GenericAPIView, UpdateModelMixin, RetrieveModelMixin):
#     queryset = Profile.objects.all()
#     serializer_class = ProfileSerializer
        
#     def get(self, request, *args, **kwargs):
#         return self.retrieve(request, *args, **kwargs)

#     def put(self, request, *args, **kwargs):
#         return self.partial_update(request, *args, **kwargs)

class ProfileView(GenericAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
        
    def get(self, request, *args, **kwargs):
        user = User.objects.filter(username=self.kwargs["user"])
        if user: 
            user = user[0]
            instance = Profile.objects.filter(user=user)
            if instance:
                instance = instance[0]
                serializer = self.get_serializer(instance)
                return Response(serializer.data)
        else:
            return Response({"Status": "This user doesn't exist"})

    def put(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

