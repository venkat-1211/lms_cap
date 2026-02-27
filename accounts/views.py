from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import RegisterSerializer, LoginSerializer
from core.responses import success

from rest_framework.permissions import AllowAny
from rest_framework_simplejwt.views import TokenObtainPairView


class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return success(message="User Registered", data={"email": user.email})


class LoginView(TokenObtainPairView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data["user"]

        refresh = RefreshToken.for_user(user)

        return success(data={
            "access": str(refresh.access_token),
            "refresh": str(refresh)
        })