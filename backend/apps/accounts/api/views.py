from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer

# Register user view
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

# Login View
class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

# Logout view
class LogoutView(generics.GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        refresh_token = request.data.get("refresh")from rest_framework import status, generics, permissions
        from rest_framework.response import Response
        from rest_framework.permissions import AllowAny
        from rest_framework_simplejwt.views import TokenObtainPairView
        from rest_framework_simplejwt.tokens import RefreshToken
        from .serializers import RegisterSerializer, CustomTokenObtainPairSerializer
        
        if not refresh_token:
            return Response({ "detail": "Refresh token is required" }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response({ "detail": "Logout successfull." }, status=status.HTTP_205_RESET_CONTENT)
        except Exception:
            # internal errors hidden to clients
            return Response({ "detail": "Invalid refresh token." }, status=status.HTTP_400_BAD_REQUEST)
        