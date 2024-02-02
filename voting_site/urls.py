from django.contrib import admin
from django.urls import path
from voting_app import views
from voting_site import settings
from django.conf.urls.static import static

handler404 = 'voting_app.views.handler404'

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
    path('user_options_list/<int:user_id>/', views.user_votes, name='user_options_list'),
    path('create_claim/<int:voting_id>/', views.create_claim, name='create_claim'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)