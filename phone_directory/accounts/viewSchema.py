from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from utils.myutils import isEmailRegistered, isPasswordValid

def isValidEmail(email):
    if isEmailRegistered(email=email):
        raise ValidationError(
            'We cannot proceed with this email.')
    return email


def checkPassword(password):
    if not isPasswordValid(password):
        raise ValidationError(
            "Password is very weak. Please enter your password such " +
            "that it includes at least one digit, " +
            "one uppercase & one lowercase letter " +
            "and one special character[$@#]")


class UserPasswordChangeViewSchema(serializers.Serializer):
    oldPassword = serializers.CharField(
        help_text="Your old password", required=True)
    newPassword = serializers.CharField(
        help_text="Your new password", required=True,
        validators=[checkPassword])


class RefreshTokenSchema(serializers.Serializer):
    refresh_token = serializers.CharField(
        help_text="Refresh Token", required=True)

class TokenSchema(serializers.Serializer):
    refresh = serializers.CharField(help_text="Refresh Token", required=True)
    access = serializers.CharField(help_text="Access Token", required=True)

class AuthSuccessSchema(serializers.Serializer):
    status = serializers.CharField(help_text="Request Status (True/False)")
    data = TokenSchema()