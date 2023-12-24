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
]
