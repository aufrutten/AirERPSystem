from django.contrib.auth import login, logout
from django.contrib.auth import get_user_model

from rest_framework.viewsets import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView, Response, status

from . import permissions, serializers

# TODO: to add the throttles for each view


class AccountAuthView(APIView):
    """Account login view by credentials and logout"""
    queryset = get_user_model().objects

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAnonymousOnly()]
        return [permissions.IsAuthenticated()]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.auth.LoginSerializer
        return serializers.auth.LogoutSerializer

    def post(self, request, *args, **kwargs):
        """POST for login unauthorized user"""
        serializer = self.get_serializer_class()(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        login(request, serializer.instance, backend='django.contrib.auth.backends.ModelBackend')
        return Response(serializer.data, status=status.HTTP_200_OK, headers=self.headers)

    def delete(self, request, *args, **kwargs):
        """DELETE for logout authorized user"""
        serializer = self.get_serializer_class()(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        logout(request)
        return Response(serializer.data, status=status.HTTP_204_NO_CONTENT, headers=self.headers)


class CreateAccountView(mixins.CreateModelMixin, GenericViewSet):
    """Registering account in the system. And sending email to confirm ownership"""
    queryset = get_user_model().objects
    serializer_class = serializers.account.CreateAccountSerializer
    permission_classes = [permissions.IsAnonymousOnly]


class ResetPasswordView(GenericAPIView):
    queryset = get_user_model().objects
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.account.ForgotPasswordSerializer
        return serializers.account.ChangePasswordSerializer

    def post(self, request):
        """Sending email with redirect url to UI email/token"""
        serializer = self.get_serializer_class()(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK, headers=self.headers)

    def put(self, request):
        """Setting new password to user if token is valid to that email; Token is required"""
        serializer = self.get_serializer_class()(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=self.headers)


class AccountConfirmView(GenericAPIView):
    queryset = get_user_model().objects
    serializer_class = serializers.account.ConfirmEmailSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Activating account and redirect to main page of UI"""
        serializer = self.get_serializer_class()(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        login(request, serializer.instance, backend='django.contrib.auth.backends.ModelBackend')
        return Response(serializer.data, status=status.HTTP_200_OK, headers=self.headers)


class AccountView(mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """Read Update Delete view off account"""
    queryset = get_user_model().objects
    serializer_class = serializers.account.AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = self.queryset.filter(email=self.request.user).first()
        self.check_object_permissions(self.request, obj)
        return obj


class AccountSocialAuthView(GenericAPIView):
    """Third Sign In OAuth2"""
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'PUT':
            return serializers.OAuth2.PUTSerializer
        return serializers.OAuth2.GETSerializer

    def get(self, request, social_backend):
        """
        Return the client_id of OAuth backend.
        if write "all" it returns all available social methods authentications
        """
        context = {'request': request, 'social_backend': social_backend}
        serializer = self.get_serializer_class()(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK, headers=self.headers)

    def put(self, request, social_backend):
        """Return the access_token and refresh_token"""
        context = {'request': request, 'social_backend': social_backend}
        serializer = self.get_serializer_class()(data=request.data, context=context)
        serializer.is_valid(raise_exception=True)

        login(request, serializer.instance, backend='django.contrib.auth.backends.ModelBackend')

        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=self.headers)
