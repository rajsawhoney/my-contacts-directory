from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework import status, permissions, generics
from drf_yasg.utils import swagger_auto_schema
from django.db import transaction

from .models import User
from .serializers import UserSerializer

from .viewSchema import (AuthSuccessSchema,
                         RefreshTokenSchema,
                         UserPasswordChangeViewSchema
                         )

AppName = "My Contacts Directory"


class UserDetailView(generics.RetrieveAPIView):
    serializer_class = UserSerializer
    queryset = User.objects.all()
    
class RegisterUser(APIView):
    '''User Registeration View'''
    permission_classes = (permissions.AllowAny, )

    @swagger_auto_schema(request_body=UserSerializer,
                         responses={200: AuthSuccessSchema})
    # makes sure that a user instance is created
    # only if each data required are valid
    @transaction.atomic()
    def post(self, request, format='json'):
        '''Takes name,phone,email,password'''
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            user = serializer.save()
            if user:
                token_data = user.tokens()
                return Response({
                    'status': True,
                    'data':token_data
                },
                    status=status.HTTP_201_CREATED)
        return Response({
            'status': False,
            'message': serializer.errors
        },
            status=status.HTTP_400_BAD_REQUEST)


class LogoutAndBlacklistRefreshTokenForUserView(APIView):  # User logout view
    '''The user must call this api with refresh_token
    as body parameter to unauthenticate himself/herself'''
    permission_classes = (permissions.AllowAny, )

    @swagger_auto_schema(request_body=RefreshTokenSchema)
    def post(self, request):
        try:
            refresh_token = request.data.get('refresh_token', False)
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(
                {
                    'status': True,
                    'message': 'User logged out successfully.'
                },
                status=status.HTTP_200_OK)
        except Exception as e:
            return Response(
                {
                    'status': False,
                    'code': "invalid_token",
                    'message': f"Failed to log the user out. {e}"
                },
                status=status.HTTP_400_BAD_REQUEST)


class UserPasswordChange(APIView):
    '''
        Password Change By Only Authorised User
    '''

    # Only an authenticated user can change password
    permission_classes = (permissions.IsAuthenticated, )

    @swagger_auto_schema(request_body=UserPasswordChangeViewSchema,
                         responses={200: None})
    def put(self, request):
        success_status = False
        response_message = None
        http_code = None
        serializer = UserPasswordChangeViewSchema(data=request.data)
        if serializer.is_valid(raise_exception=False):
            user_instance = request.user
            oldPassword = request.data.get('oldPassword')
            newPassword = request.data.get('newPassword',
                                           user_instance.password)
            if user_instance.check_password(oldPassword.strip()):
                '''if old password matches'''
                from django.contrib.auth import update_session_auth_hash
                user_instance.set_password(newPassword.strip())
                update_session_auth_hash(request, user_instance)
                user_instance.save()
                success_status = True
                http_code = status.HTTP_202_ACCEPTED
                response_message = "Password changed successfully!"
            else:
                success_status = False
                http_code = status.HTTP_400_BAD_REQUEST
                response_message = "Old password not matching!!"

        else:
            success_status = False
            http_code = status.HTTP_400_BAD_REQUEST
            response_message = serializer.errors
        return Response({
            'status': success_status,
            'message': response_message
        },
            status=http_code)


class GetCurrentUser(APIView):
    '''Only an authorised user can access this API and
        it returns the currently authenticated user
        Accept GET request with header Authorisation
        Bearer <access token>
    '''
    serializer_class = UserSerializer
    permission_classes= [
        permissions.IsAuthenticated,
    ]
    
    def get(self, request):
        user = UserSerializer(instance=request.user)
        return Response(data={
            "status": True,
            "data": user.data
        },
            status=status.HTTP_200_OK)
