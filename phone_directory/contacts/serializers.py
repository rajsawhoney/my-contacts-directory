from rest_framework import serializers
from accounts.models import User
from accounts.serializers import UserSerializer
from .models import Contact

class ContactSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact
        fields = ('id', 'label', 'phone', 'is_spam')

class ContactOwnerWithEmailSerializer(UserSerializer):
    class Meta:
        model = User
        fields = ('id','name', 'email')

class ContactOwnerWithoutEmailSerializer(UserSerializer):
    email = serializers.SerializerMethodField()
    
    def get_email(self, obj):
        return 'no access'
    
    class Meta:
        model = User
        fields = ('id', 'name', 'email')


class SearchResultSerializer(ContactSerializer):
    owner = serializers.SerializerMethodField()

    def get_owner(self, obj):
        # Makes sure only the user who is already
        # inside the that user's contact list has access to email
        if self.context:
            if not self.context.get('request').user.has_access_to_email(obj.owner()):
                return ContactOwnerWithoutEmailSerializer(instance=obj.owner()).data
        return ContactOwnerWithEmailSerializer(instance=obj.owner()).data

    class Meta:
        model = Contact
        fields = ('id', 'phone', 'is_spam', 'owner')
