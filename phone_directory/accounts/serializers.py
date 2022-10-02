from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from .models import User
from utils.myutils import (
    isEmailRegistered, isPhoneRegistered,
    isPasswordValid, normalizePhone)

class UserSerializer(serializers.ModelSerializer):
    """
        User Serializer
    """
    id = serializers.CharField(read_only=True)
    email = serializers.SerializerMethodField()
    
    def get_email(self,obj):
        # Makes sure only the user who is already
        # inside the that user's contact list has access to email
        if self.context:
            if not self.context.get('request').user.has_access_to_email(obj):
                return 'no access'
        return obj.email
    
    def validate_phone(self, value):
        if isPhoneRegistered(value):
            raise ValidationError("Phone already taken!")
        return value

    def validate_email(self, value):
        if isEmailRegistered(value):
            raise ValidationError("Email already taken!")
        return value

    def validate_password(self, value):
        if not isPasswordValid(value):
            raise ValidationError(
                "Password is very weak." +
                " Please enter your password such" +
                " that it consists of min 8 length including" +
                " at least one digit, one upper-case & one " +
                "lowercase letter and one special character[$@#]"
            )
        return value

    class Meta:
        model = User
        fields = ('id', 'name', 'email', 'phone', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        phone = validated_data.pop('phone', None)
        phone = normalizePhone(phone)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        if phone is not None:
            instance.phone = phone
        instance.save()
        return instance

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        if password is not None:
            instance.set_password(password)
        return super().update(instance, validated_data)