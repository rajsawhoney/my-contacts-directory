from django.db import models
from django.dispatch import receiver
from django.db.models.signals import pre_save, post_save
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import (
    AbstractBaseUser, PermissionsMixin, BaseUserManager
)
from django.utils import timezone
from django.forms import ValidationError
from contacts.models import Contact
from utils.myutils import (
    isValidPhone, isPasswordValid, normalizePhone,
    generate_unique_user_id
)
# Create your models here.


def checkPhoneNum(phone):
    if not isValidPhone(phone):
        raise ValidationError(
            "Invalid Phone Number! Please enter correct phone number e.g. 9*********"
        )
    return phone


def checkPassword(password):
    if not isPasswordValid(password):
        raise ValidationError(
            "Password is very weak. Please enter your password such"
            + "that consists of min 8 length including"
            + " at least one digit, one uppercase letter,one"
            + "lowercase letter,one special character[$@#]"
        )
    return password


class UserManager(BaseUserManager):

    def addContact(self, user, contact):
        user.contacts.add(contact)

    def removeContact(self, user, contact):
        user.contacts.remove(contact)

    def _create_user(
        self, name, phone, email, password, is_staff, is_superuser, **extra_fields
    ):
        """
        Creates and saves a User with the given name, email and password.
        """
        if not phone:
            raise ValueError(
                {"status": False, "message": "Phone number is required!"})
        if not name:
            raise ValueError(
                {"status": False, "message": "Please enter correct name!"})
        checkPassword(password)
        phone = normalizePhone(phone)
        email = email if self.normalize_email(email) else None
        user = self.model(
            name=name,
            phone=phone,
            email=email,
            is_staff=is_staff,
            is_active=True,
            is_superuser=is_superuser,
            created_at=timezone.now(),
            **extra_fields,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, name, phone, email=None, password=None, **extra_fields):
        if not name:
            raise ValueError(
                {"status": False, "message": "Please enter correct name!"})
        checkPassword(password)
        return self._create_user(
            name, phone, email, password, False, False, **extra_fields
        )

    def create_superuser(self, name, phone, password, **extra_fields):
        if not name:
            raise ValueError(
                {"status": False, "message": "Please enter correct name!"})
        checkPassword(password)
        return self._create_user(
            name=name, phone=phone, email=None, password=password, is_superuser=True, is_staff=True, **extra_fields
        )


class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(
        "User Id", max_length=50, unique=True, blank=True, primary_key=True
    )
    name = models.CharField(max_length=150)
    contacts = models.ManyToManyField(
        'contacts.Contact', related_name='user_by_contact', blank=True)
    phone = models.CharField(
        validators=[checkPhoneNum], max_length=15, unique=True)
    email = models.EmailField(
        "Email",
        max_length=254,
        unique=True,
        blank=True,
        null=True
    )
    created_at = models.DateTimeField("Created At", auto_now_add=True)

    is_staff = models.BooleanField(default=False)
    is_blocked = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_online = models.DateTimeField(auto_now=True)

    USERNAME_FIELD = "phone"
    REQUIRED_FIELDS = ("name", "password")
    objects = UserManager()

    def __str__(self):
        return f"{self.name} ({self.phone})"

    def get_all_contacts(self):
        return self.contacts.all()

    def has_access_to_email(self, owner):
        try:
            query = owner.contacts.all().filter(phone=self.phone)
            return query.exists()
        except:
            return False

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {"refresh": str(refresh), "access": str(refresh.access_token)}

    class Meta:
        managed = True
        verbose_name = 'User'
        verbose_name_plural = 'Users'


@receiver(pre_save, sender=User)
def user_pre_save_receiver(sender, instance, **kwargs):
    if not instance.id:
        instance.id = generate_unique_user_id(instance)


@receiver(post_save, sender=User)
def user_post_save_receiver(sender, instance, created, **kwargs):
    if created:
        new_contact, _ = Contact.objects.get_or_create(phone=instance.phone, defaults={
            'label': f"{instance.name}'s primary phone no."})
        User.objects.addContact(instance, new_contact)
