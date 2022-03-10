from django.urls import path, include
from .views import Register_Users, Login_Users, ProfileView

urlpatterns = [
    path('register/', Register_Users.as_view(), name='register-users'),
    path('login/', Login_Users.as_view(), name='login-users'),
    path('profile/<str:user>/', ProfileView.as_view(), name='profile-view'),
    path('password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
]