from rest_framework import generics, filters, decorators, permissions, status, response
from django_filters import rest_framework as dg_filters
from .models import Contact
from .serializers import ContactSerializer, SearchResultSerializer
from accounts.models import User

class UserContactsListView(generics.ListAPIView):
    serializer_class = ContactSerializer
    permission_classes= [permissions.IsAuthenticated,]

    def get_queryset(self):
        '''returns contacts for the current user'''
        return self.request.user.get_all_contacts()


class ContactsFilter(dg_filters.FilterSet):
    class Meta:
        model = Contact
        fields = ('phone', 'user_by_contact', 'is_spam',)


class SearchUserView(generics.ListAPIView):
    queryset = Contact.objects.all()
    serializer_class = SearchResultSerializer
    filter_backends = [filters.SearchFilter]
    permission_classes= [permissions.IsAuthenticated,]
    search_fields = ['phone','user_by_contact__name']
    
@decorators.api_view(['PUT'])
@decorators.permission_classes([permissions.IsAuthenticated, ])
def mark_as_spam(request, id):
    if id is not None:
        contact_query = Contact.objects.filter(id=id)
        if contact_query.exists():
            Contact.objects.mark_as_spam(contact_query.first())
            return response.Response({
                'status': True,
                'is_spam':True,
                'message': 'Contact marked as spam successfully.'
            },
                status=status.HTTP_201_CREATED)
        else:
            return response.Response({
                'is_spam':False,
                'status': False,
                'message': "Contact instance not found!"
            },
                status=status.HTTP_400_BAD_REQUEST)
    return response.Response({
        'status': False,
        'message': 'Contact Id is missing'
    },
        status=status.HTTP_400_BAD_REQUEST)

class CreateContactView(generics.GenericAPIView):
    '''View to create a contact
    '''
    serializer_class = ContactSerializer
    permission_classes= [
        permissions.IsAuthenticated,
    ]
    
    def post(self, request):
        serializer = ContactSerializer(data=request.data)
        if serializer.is_valid(raise_exception=False):
            contact = serializer.save()
            User.objects.addContact(request.user,contact)
            return response.Response(data={
                "status": True,
                "data": ContactSerializer(instance=contact).data
            },
                status=status.HTTP_200_OK)
        else:
            return response.Response({
        'status': False,
        'message': serializer.errors
    },
        status=status.HTTP_400_BAD_REQUEST)    
            
@decorators.api_view(['GET'])
@decorators.permission_classes([permissions.IsAuthenticated, ])
def check_spam_number(request, phone_number):
    if phone_number is not None:
        contact_query = Contact.objects.filter(phone=phone_number)
        if contact_query.exists():
            return response.Response({
                'status': True,
                'is_spam': contact_query.first().is_spam
            },
                status=status.HTTP_200_OK)
        else:
            return response.Response({
                'status': False,
                'message': "Phone number not found in our database!"
            },
                status=status.HTTP_400_BAD_REQUEST)
            
    return response.Response({
        'status': False,
        'message': 'Please specify a phone number!'
    },
        status=status.HTTP_400_BAD_REQUEST)
