from django.conf import settings
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import ensure_csrf_cookie

from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.views import APIView

from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenRefreshSerializer
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer


# Registration view
class RegisterView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "success": True,
                "message": "User registered successfully",
                "data": {
                    "id": user.id,
                    "email": user.email,
                    "username": user.username,
                },
            },
            status=status.HTTP_201_CREATED
        )

# Custom Login: set refresh token in httpOnly cookie, return only access + user info in JSON
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        # Use parent to validate credentials and get tokens
        response = super().post(request, *args, **kwargs)
        refresh = response.data.get("refresh")

        if refresh:
            # Set httpOnly cookie for refresh token, remove refresh from JSON payload
            response.set_cookie(
                key="refresh_token",
                value=refresh,
                httponly=True,
                secure=getattr(settings, "SECURE_COOKIE", False),
                samesite="Strict",
                max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
                path="/api/auth/"
            )
            response.data.pop("refresh", None)
        return response


# Refresh: read refresh token from cookie, return new access; rotate cookie if serializer returns new refresh
class CookieTokenRefreshView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get("refresh_token")
        if not refresh_token:
            return Response({ "detail": "Refresh token missing" }, status=status.HTTP_401_UNAUTHORIZED)
        
        serializer = TokenRefreshSerializer(data={ "refresh": refresh_token })
        serializer.is_valid(raise_exception=True)
        data = serializer.validated_data  # contains 'access' (and possibly 'refresh')

        response = Response({ "access": serializer.data.get("access") }, status=status.HTTP_200_OK)

        # Sets the new refresh token cookie, if the refresh totation occurred
        new_refresh = serializer.data.get("refresh")
        if new_refresh:
            response.set_cookie(
                key="refresh_token",
                value=new_refresh,
                httponly=True,
                secure=getattr(settings, "SECURE_COOKIE", False),
                samesite="Strict",
                max_age=int(settings.SIMPLE_JWT["REFRESH_TOKEN_LIFETIME"].total_seconds()),
                path="/api/auth/",
            )
        
        return response

# Logout: blacklist refresh token (from cookie or request body)
class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.COOKIES.get("refresh_token")
     
        if not refresh_token:
            return Response({ "detail": "Refresh token is required" }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            response = Response({ "detail": "Logout successfull." }, status=status.HTTP_205_RESET_CONTENT)
            response.delete_cookie("refresh_token", path="/api/auth/")
            return response
            
        except Exception:
            # internal errors hidden to clients
            return Response({ "detail": "Invalid refresh token." }, status=status.HTTP_400_BAD_REQUEST)
    

# Helper endpoint - ensure csrf is set
class EnsureCSRFCookieView(APIView):
    permission_classes = [permissions.AllowAny]

    @method_decorator(ensure_csrf_cookie)
    def get(self, request, *args, **kwargs):
        return Response({"detail": "CSRF cookie set"})