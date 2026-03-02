# views_auth.py
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from datetime import timedelta
from django.conf import settings
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import views

class CookieTokenObtainPairView(TokenObtainPairView):
    serializer_class = TokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        access = serializer.validated_data["access"]
        refresh = serializer.validated_data["refresh"]

        response = Response({"detail": "Login successful"}, status=status.HTTP_200_OK)

        # Set HTTP-only cookies
        response.set_cookie(
            key="access",
            value=access,
            httponly=True,
            secure=settings.DEBUG is False,  # IMPORTANT in production
            samesite="Lax" if not settings.DEBUG else None,
            max_age=60 * 60,  # 1 hour
        )

        response.set_cookie(
            key="refresh",
            value=refresh,
            httponly=True,
            secure=settings.DEBUG is False,
            samesite="Lax" if not settings.DEBUG else None,
            max_age=7 * 24 * 60 * 60,  # 7 days
        )

        return response
    

class CookieTokenRefreshView(TokenRefreshView):

    def post(self, request, *args, **kwargs):
        refresh = request.COOKIES.get("refresh")

        if not refresh:
            return Response({"detail": "No refresh token"}, status=401)

        serializer = self.get_serializer(data={"refresh": refresh})
        serializer.is_valid(raise_exception=True)

        access = serializer.validated_data["access"]

        response = Response({"detail": "Token refreshed"})
        response.set_cookie(
            key="access",
            value=access,
            httponly=True,
            secure=True,
            samesite="Lax",
            max_age=60 * 60,
        )

        return response
    
class CookieLogoutView(views.APIView):
    def post(self, request, *args, **kwargs):
        response = Response({"detail": "Logout successful"}, status=status.HTTP_200_OK)
        
        # Clear access token cookie
        response.delete_cookie(
            key="access",
            path="/",
            domain=settings.SESSION_COOKIE_DOMAIN,  # Optional: set if using subdomains
            samesite="Lax" if not settings.DEBUG else None,
        )
        
        # Clear refresh token cookie
        response.delete_cookie(
            key="refresh",
            path="/",
            domain=settings.SESSION_COOKIE_DOMAIN,
            samesite="Lax" if not settings.DEBUG else None,
        )
        
        return response