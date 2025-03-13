from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views

urlpatterns = [    
    path('', views.index, name='index'),  
    path('add/<int:num1>/<int:num2>', views.add, name='add'),
    path('operation/', views.operation, name='operation'),
    path('sum_multiples/', views.sum_multiples, name = 'sum_multiples'),
    path('tasks_form/', views.TasksListCreate.as_view(), name = 'tasks_view_create'),
    path('tasks/', views.TasksList.as_view(), name = 'tasks_view'),
    path('tasks/<int:pk>/', views.TasksRetrieveUpdateDestory.as_view(), name = 'tasks_update'),
    path('create_user/', views.UserCreate.as_view(), name='user_create'),
    path('users/<int:pk>/', views.AccountsRetrieveUpdateDestory.as_view(), name = 'accounts_update'),
    path('create/', views.create_account, name = 'account_create'),
    path('create/successful_account.html', views.account_success, name = 'account_created_success'),
    path('api/token/', jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/tokenize/', views.CustomTokenObtainView.as_view(), name='token_obtain_pair'),
    path('api/tokenizers/', views.CustomTokenObtainProtectedInfo.as_view(), name='token_obtain_pair')
    ]