from django.db import models
from django.forms import ValidationError
from django.dispatch import receiver
from django.db.models.signals import pre_save
from utils.myutils import isValidPhone,generate_unique_user_id
# Create your models here.

def checkPhoneNum(phone):
    if not isValidPhone(phone):
        raise ValidationError(
            "Invalid Phone Number! Please enter correct phone number e.g. 9*********"
        )
    return phone

class ContactManager(models.Manager):
    def mark_as_spam(self,contact):
        contact.is_spam = True
        contact.save()


class Contact(models.Model):
    id = models.CharField(
        "Contact Id", max_length=50, unique=True, blank=True, primary_key=True
    )
    label = models.CharField(max_length=150)
    phone = models.CharField(
        validators=[checkPhoneNum], max_length=15, unique=True)
    is_spam = models.BooleanField(default=False)
    
    objects = ContactManager()
    
    def owner(self):
        return self.user_by_contact.first()

    def __str__(self):
        return self.label + '('+self.phone+')'

    class Meta:
        managed = True
        verbose_name = 'Contact'
        verbose_name_plural = 'Contacts'

@receiver(pre_save, sender=Contact)
def user_pre_save_receiver(sender, instance, **kwargs):
    if not instance.id:
        instance.id = generate_unique_user_id(instance)
