from django.http import JsonResponse
from django.shortcuts import render
from django.views import View

from appointment.models import Contact

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.authentication import JWTAuthentication
from user.models import Student
from user.serializers import UserSerializer
from django.contrib.auth import authenticate, login, logout
from rest_framework.views import APIView
from rest_framework import permissions
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from django.db.models import Q
from rest_framework.authentication import SessionAuthentication

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['user'] = UserSerializer(user).data
        return token

    def validate(self, attrs):
        username = attrs.get('username')
        password = attrs.get('password')
        request = self.context.get('request')

        print("checkkk", username, password, request)
        if request:
            user = authenticate(request=request, username=username, password=password)
            if user:
                login(request, user)
        else:
            print("Request object is None.")

        data = super().validate(attrs)
        return data
    

class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer




class SignUp(APIView):
    permission_classes = (permissions.AllowAny, )
    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            if user.is_authenticated:
                return JsonResponse({'success': False, 'msg': "You are already authenticated. Refresh the page"})
            username = request.data.get('username', '').strip()
            first_name = request.data.get('first_name', '').strip()
            last_name = request.data.get('last_name', '').strip()
            password = request.data.get('password', '').strip()
            email = request.data.get('email', '').strip()
            verify_pass = request.data.get('verifyPassword', '').strip()
            country = request.data.get('country', '').strip()
            intake = request.data.get('intake', '').strip()
            grad_type = request.data.get('grad_type', '').strip()
            phone_number = request.data.get('phone_number', '').strip()

            if not username or not first_name or not last_name or not password or not email or not verify_pass\
                or not country or not intake or not grad_type or not phone_number:
                return JsonResponse({'success': False, 'msg': "Please enter all details."})

            if password != verify_pass:
                return JsonResponse({'success': False, 'msg': "Both passwords should match"})

            if User.objects.filter(Q(username=username) | Q(email=email)).exists():
                return JsonResponse({'success': False, 'msg': "Username/email already registered. Please try with another username/email."})

            user = User.objects.create_user(
                username=username,
                last_name=last_name,
                first_name=first_name,
                password=password,
                email=email
            )

            Student.objects.create(
                user=user,
                country=country,
                grad=grad_type,
                intake=intake,
                phone_number=phone_number,
            )

            authenticated_user = authenticate(request, username=username, password=password)
            if not authenticated_user:
                return JsonResponse({'success': False, 'msg': "Failed to authenticate user."})

            refresh = RefreshToken.for_user(user)    
            access_token = str(refresh.access_token)

            token_serializer = MyTokenObtainPairSerializer(data={'username': user.username, 'password': password})
            token_serializer.is_valid(raise_exception=True)

            login(request, authenticated_user)
            return JsonResponse({'success': True, 'msg': "User Created", "user": UserSerializer(user).data,
                                    "token": {'access_token': access_token, 'refresh_token': str(refresh)}})

        except Exception as e:
            print('err while creating user', str(e))
            return JsonResponse({'success': False, 'msg': "err: " + str(e)})


class SignIn(APIView):
    permission_classes = (permissions.AllowAny, )

    def post(self, request, *args, **kwargs):
        try:
            user = request.user
            print('kkkk', user.is_authenticated)
            if user.is_authenticated:
                return JsonResponse({'success': False, 'msg': "You are already authenticated. Refresh the page"})
            username = request.data.get('username')
            password = request.data.get('password')
            if not User.objects.filter(username=username).exists():
                return JsonResponse({'success': False, 'msg': "Username is not registered. Please Sign up first."})
            user = authenticate(request, username=username, password=password)
            print("userrr", user)
            if user:
                login(request, user)
                return JsonResponse({'success': True, 'msg': "Sign up successful!"})
            print(request.user)
            return JsonResponse({'success': True, 'msg': "Couldn't signin due to an error. Please try again later"})
        except Exception as e:
            print('err while creating user', str(e))
            return JsonResponse({'success': False, 'msg': "err: " + str(e)})


class LogOut(APIView):
    def post(self, request, *args, **kwargs):
        try:
            logout(request)
            return JsonResponse({'success': True, 'msg': "Logged out!"})
        except Exception as e:
            print('err while creating user', str(e))
            return JsonResponse({'success': False, 'msg': "err: " + str(e)})



class Index(View):
    def get(self, request):
        return render(request, 'index.html')

class About(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'about.html')
    
class ContactUs(View):
    def get(self, request, *args, **kwargs):
        return render(request, 'contact_us.html')
    
    def post(self, request, *args, **kwargs):
        name = request.POST.get('name', '').strip()
        email = request.POST.get('email', '').strip()
        subject = request.POST.get('subject', '').strip()
        message = request.POST.get('message', '').strip()

        if not name or not email or not subject or not message:
            return render(request, 'contact_us.html', {'error': 'All fields are required'})
        
        Contact.objects.create(
            name=name,
            email=email,
            subject=subject,
            message=message,
        )
        return JsonResponse(status=200)
        return render(request, 'contact_us.html', {'success': 'Message sent successfully'})