from django.urls import path
from .views import RegisterView, CustomTokenObtainPairView, CookieTokenRefreshView, LogoutView, EnsureCSRFCookieView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path("auth/register/", RegisterView.as_view(), name="auth_register"),
    path("auth/login/", CustomTokenObtainPairView.as_view(), name="auth_login"),
    path("auth/refresh/", CookieTokenRefreshView.as_view(), name="auth_refresh"),
    path("auth/logout/", LogoutView.as_view(), name="auth_logout"),
    path("auth/csrf/", EnsureCSRFCookieView.as_view(), name="auth_csrf"),
]
