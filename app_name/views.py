from django.shortcuts import HttpResponse, render
from . import sum_multiple_extracted
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import *
from .serializers import *
from django.shortcuts import render, redirect
from .forms import AccountsForm
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework_simplejwt.tokens import RefreshToken
from django.http import JsonResponse
from django.contrib.auth import authenticate
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from django.contrib.auth import get_user_model
import jwt
from django.conf import settings


# This function returns hello world on the webpage
def index(request): 
    return HttpResponse("Hello, world")

# This function adds two numbers that are passed into the url
def add(request, num1, num2):
    sum = num1 + num2
    return HttpResponse(f"The sum of {num1} and {num2} is {sum}.")

# This function takes a string and depending on the string applies one of +-*/ to the two numbers
def operation(request): 
    action = request.GET.get('action')  # For str: action
    num1 = int(request.GET.get('num1'))  # For int: num1
    num2 = int(request.GET.get('num2'))  # For int: num2
    result = 0
    if action == 'add':
        result = num1 + num2
    elif action == 'sub':
        result = num1 - num2
    elif action == 'mult':
        result = num1 * num2
    elif action == 'div':
        result = num1 / num2
    else:
        result = 'operator not found, please use one of: add, sub, mult, or div'
    return HttpResponse(f"The result of {action}ing {num1} and {num2} is {result}.")

# Here we get the two numbers passed into the url and pass it onto a helped method
def sum_multiples(request): 
    num1 = int(request.GET.get('num1'))  # For int: num1
    num2 = int(request.GET.get('num2'))  # For int: num2
    return HttpResponse(sum_multiple_extracted.main(num1, num2))

# In this class I use the Django generics and serializer to have a front-end UI to create and view tasks added
class TasksListCreate(generics.ListCreateAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer

# I added a delete button to the page 
    def delete(self, request, *args, **kwargs):
        Tasks.objects.all().delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

# You can view a single task by looking up a primary key
class TasksRetrieveUpdateDestory(generics.RetrieveUpdateDestroyAPIView):
    queryset = Tasks.objects.all()
    serializer_class = TasksSerializer
    lookup_field = "pk"

class TasksList(APIView):
    # If you pass in /tasks/?name=___ you can view the tasks assigned to any one person
    def get(self, request, format=None):
        # Get the name from the query parameters (if none default to empty string)
        passed_name = str(request.GET.get("name", ""))
        tasks = None
        if passed_name:
            # Filter the queryset based on the name
            tasks = Tasks.objects.filter(name__icontains=passed_name)
        else:
            # If no name, return all
            tasks = Tasks.objects.all()
        serializer = TasksSerializer(tasks, many = True)
        return HttpResponse(serializer.data, status=status.HTTP_200_OK)
    
    # You can post via an API/Postman
    def post(self, request, format=None):
        serializer = TasksSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  # This will save the task if the data is valid
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class UserCreate(generics.ListCreateAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer

    def delete(self, request, *args, **kwargs):
        Accounts.objects.all().delete()
        return HttpResponse(status=status.HTTP_204_NO_CONTENT)

class AccountsRetrieveUpdateDestory(generics.RetrieveUpdateDestroyAPIView):
    queryset = Accounts.objects.all()
    serializer_class = AccountsSerializer
    lookup_field = "pk"

def create_account(request):
    permission_classes = (IsAuthenticated, ) 
    if request.method == 'POST':
        form = AccountsForm(request.POST)
        if form.is_valid():
            form.save()  # Save the form data to the database
            return redirect('account_created_success')  # Redirect to a success page after submission
    else:
        form = AccountsForm()
    return render(request, 'add_account.html', {'form': form})

def account_success(request):
    return render(request, 'successful_account.html')

class CustomTokenObtainView(APIView):
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)

        if user is None:
                    return JsonResponse({'error': 'Invalid username or password'}, status=400)
        
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        data = {
            'first name': user.first_name,
            'last name': user.last_name,
            'username': user.username, 
            'token': access_token
        }
        return JsonResponse(data)
    
class CustomTokenObtainProtectedInfo(APIView):
    def post(self, request, *args, **kwargs):
        token = request.headers.get('Authorization')

        if not token:
            return Response({'error': 'Token is required in the Authorization header'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            # Decode and verify the token using the public key or secret
            if token:
                token = token.split(' ')[1]  # This line will fail if there's no "Bearer"
                print(token)
            else:
                return Response({'error': 'Token is required in the Authorization header'}, status=status.HTTP_400_BAD_REQUEST)
            decoded_token = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            print(decoded_token, 'DECODED')
            # Get the user based on the user_id stored in the JWT
            user_id = decoded_token.get('user_id')
            user = Accounts.objects.get(id=user_id)
            type(user.phone)
            data = {
                'first_name': user.first_name,
                'last_name': user.last_name,
                'email': user.email,
                'phone': str(user.phone)
            }

            type(user.phone)

            return Response(data, status=status.HTTP_200_OK)

        except jwt.ExpiredSignatureError:
            return Response({'error': 'Token has expired'}, status=status.HTTP_401_UNAUTHORIZED)

        except jwt.DecodeError:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        except Accounts.DoesNotExist:
            return Response({'error': 'User not found with the information in the token'}, status=status.HTTP_404_NOT_FOUND)