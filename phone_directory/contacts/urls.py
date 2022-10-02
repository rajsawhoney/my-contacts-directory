from django.urls import path
from . import views
urlpatterns = [
    path('mark_as_spam/<str:id>',views.mark_as_spam,name='mark_as_spam'),
    path('check_spam_number/<str:phone_number>',views.check_spam_number,name='check_spam_number'),
    path('mycontacts/',views.UserContactsListView.as_view(),name='mycontacts'),
    path('create/',views.CreateContactView.as_view(),name='create-contact'),
    path('search',views.SearchUserView.as_view(),name='search-contacts'),
]