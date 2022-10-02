from django.urls import path
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views

urlpatterns = [
    path('login/', TokenObtainPairView.as_view(), name='user-login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='user-token-refresh'),
    path('register/', views.RegisterUser.as_view(), name='user-register'),
    path('password/change/', views.UserPasswordChange.as_view(), name='user-password-change'),
    path('logout/', views.LogoutAndBlacklistRefreshTokenForUserView.as_view(), name='user-logout'),
    path('myprofile/', views.GetCurrentUser.as_view(), name='user-profile'),
    path('userdetail/<pk>', views.UserDetailView.as_view(), name='user-detail'),
]