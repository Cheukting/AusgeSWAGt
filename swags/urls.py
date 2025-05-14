from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', auth_views.LoginView.as_view(template_name='registration/login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('swag/new/', views.swag_create, name='swag_create'),
    path('swag/<int:pk>/', views.swag_detail, name='swag_detail'),
    path('swag/<int:pk>/update/', views.swag_update, name='swag_update'),
    path('my-swags/', views.user_swags, name='user_swags'),
    path('api/suggestions/', views.get_suggestions, name='get_suggestions'),
    path('api/similar-swags/', views.get_similar_swags, name='get_similar_swags'),
]
