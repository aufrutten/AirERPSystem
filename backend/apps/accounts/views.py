
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth import authenticate, login, logout

from rest_framework.viewsets import mixins
from rest_framework.generics import GenericAPIView
from rest_framework.viewsets import GenericViewSet
from rest_framework.views import APIView, Response, status

from . import permissions, serializers, utils


class AccountLoginView(APIView):
    """Account login view by credentials"""
    queryset = get_user_model().objects
    serializer_class = serializers.AccountLoginSerializer
    permission_classes = [permissions.IsAnonymousOnly]

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        login(request, authenticate(request, email=request.data['email'], password=request.data['password']))
        return Response(serializer.get_response(), status=status.HTTP_200_OK, headers=self.headers)


class AccountLogoutView(APIView):
    """Account logout APIView, required to be authenticated"""
    queryset = get_user_model().objects
    serializer_class = serializers.AccountLogoutSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        request.user.refresh_access_token()
        logout(request)
        return Response(status=status.HTTP_200_OK, headers=self.headers)


class CreateAccountView(mixins.CreateModelMixin, GenericViewSet):
    """Registering account in the system"""
    queryset = get_user_model().objects
    serializer_class = serializers.CreateAccountSerializer
    permission_classes = [permissions.IsAnonymousOnly]


class ResetPasswordView(GenericAPIView):
    queryset = get_user_model().objects
    permission_classes = [permissions.AllowAny]

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.POSTAccountResetSerializer
        return serializers.PUTAccountResetSerializer

    def post(self, request):
        """Sending email with redirect url to UI email/token"""
        serializer = self.get_serializer_class()(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.instance.email_user(**utils.RenderEmail(serializer.instance, 'reset')())
        return Response(serializer.data, status=status.HTTP_200_OK, headers=self.headers)

    def put(self, request):
        """Setting new password to user if token is valid to that email; Token is required"""
        serializer = self.get_serializer_class()(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.instance.set_password(request.data['password'])
        serializer.instance.refresh_access_token()
        return Response(serializer.data, status=status.HTTP_201_CREATED, headers=self.headers)


class AccountConfirmView(GenericAPIView):
    queryset = get_user_model().objects
    serializer_class = serializers.AccountConfirmSerializer
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        """Activating account and redirect to main page of UI"""
        serializer = self.get_serializer_class()(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.instance.activate_account(request.data['access_token'])
        user = self.queryset.filter(email=request.data['email']).first()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        return Response(serializer.data, status=status.HTTP_200_OK, headers=self.headers)


class AccountView(mixins.DestroyModelMixin, mixins.UpdateModelMixin, mixins.RetrieveModelMixin, GenericViewSet):
    """Read Update Delete view off account"""
    queryset = get_user_model().objects
    serializer_class = serializers.AccountSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        obj = self.queryset.filter(email=self.request.user).first()
        self.check_object_permissions(self.request, obj)
        return obj


class AccountSocialLoginView(GenericAPIView):
    """Third Sign In OAuth2"""
    permission_classes = [permissions.IsAnonymousOnly]
    oauth_backends = {'google-oauth2': settings.SOCIAL_AUTH_GOOGLE_OAUTH2_KEY}

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return serializers.POSTAccountSocialAuthSerializer
        return serializers.GETAccountSocialAuthSerializer

    def get(self, request, backend):
        """Return the client_id of OAuth backend. Now available: google-oauth2 (google);"""
        if backend in self.oauth_backends:
            return Response({'client_id': self.oauth_backends[backend]}, headers=self.headers)
        return Response({'detail': "OAuth isn't exist"}, status=status.HTTP_404_NOT_FOUND, headers=self.headers)

    def post(self, request, backend):
        """Return the access_token and refresh_token"""
        if backend not in self.oauth_backends:
            return Response({'detail': "OAuth isn't exist"}, status=status.HTTP_404_NOT_FOUND, headers=self.headers)
        user = utils.register_by_access_token(request, backend)
        login(request, user)
        response = {'email': user.email, 'access_token': user.access_token, 'refresh_token': user.refresh_token}
        return Response(response, headers=self.headers)
