from django.http import JsonResponse
from django.shortcuts import render
from django.contrib.auth.models import User
from rest_framework import generics
from .serializers import UserSerializer
from rest_framework.permissions import AllowAny
from rest_framework.views import APIView
from django.db.models import Q

class UserAPI(APIView):
    def get(self, request, *args, **kwargs):
        print("useee", request)
        user = request.user
        print("useee", user)
        if user.is_anonymous:
            return JsonResponse(status=401, data=dict())
        
        serialized_user = UserSerializer(user).data
        return JsonResponse(serialized_user)
    