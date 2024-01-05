from django.contrib import admin
from django.urls import path
from voting_app import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('voting/', views.voting_detail),
    path('', views.voting_list, name='voting_list'),
    path('<int:voting_id>/', views.voting_detail, name='voting_detail'),
    path('accounts/login/', views.user_login, name='login'),
    path('accounts/logout/', views.user_logout, name='logout'),
    path('create_voting/', views.create_voting, name='create_voting'),
    path('accounts/register/', views.user_register, name='register'),
    path('edit_voting/<int:voting_id>/', views.edit_voting, name='edit_voting'),
]
