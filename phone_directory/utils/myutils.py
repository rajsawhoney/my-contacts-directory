import re
import string
from django.forms import ValidationError
from django.utils import timezone
from accounts import models as acc_models

def normalizePhone(phone):
    '''chops-off the country-code if present'''
    return phone[-10:]

def isValidPhone(phone):
    phone = normalizePhone(phone)
    return (len(phone) == 10 and
            re.fullmatch(r'[\+\(]?9\d{9}', phone) is not None)

def isPasswordValid(password):
    return re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$*-+=%!`~;:<>/?\|{}^&)(,.'])[\w\d@#$*-+=%!`~;:<>/?\|{}^&)(,.']{8,30}$",
                    password)

def generate_uuid():
    import uuid
    unique_id = str(uuid.uuid4())
    return unique_id


def generate_unique_user_id(instance, new_user_uid=None):
    """
    Function to generate a unique user id
    """
    if new_user_uid is not None:
        user_uid = new_user_uid
    else:
        user_uid = generate_uuid()

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(id=user_uid).exists()
    if qs_exists:
        new_user_uid = generate_uuid()
        return generate_unique_user_id(instance, new_user_uid=new_user_uid)

    return user_uid

def isPhoneRegistered(phone):
    phone = normalizePhone(phone)
    '''Checks the DB whether the phone is registered'''
    return phone and acc_models.User.objects.filter(phone__iexact=str(phone)).exists()

def isEmailRegistered(email):
    '''Checks the DB whether the email is registered'''
    if email and email is not None:
        email = email.lower()
    return email and acc_models.User.objects.filter(email__iexact=email).exists()

def getOTPInstance(phone):
    phone = normalizePhone(phone)
    return acc_models.PhoneOTP.objects.filter(phone__iexact=str(phone))

def handleOTPSentBeforeOrNot(phone):
    ''' Checks whether any OTP is sent before or not?
        * If sent before, then it's an another request for OTP,
        so it return the same OTP Instance again and also it checks for OTP count
        i.e. if count >= 5 --> Restrict the phone number
        ** If not then generate a brand new OTP Instance and return it
    '''
    phone = normalizePhone(phone)
    old = getOTPInstance(phone)
    count = 1
    otp_ins_to_send = None
    if old.exists() and not old.first().is_expired:
        old_ins = old.first()
        if int(old_ins.count) >= 5:
            raise ValidationError(
                {'status': False, 'message': "OTP Maximum limits reached." +
                 " Kindly contact our customer care or try with different" +
                 " phone number."}, code=406)
        old_ins.count += 1
        old_ins.save()
        otp_ins_to_send = old_ins
    else:
        new_otp_ins = None
        if old.exists() and old.first().is_expired:
            '''Here we simply revive the expired otp instance
            in order to to prevent UNIQUE constraint
            failure.
            '''
            new_otp_ins = old.first()
            new_otp_ins.is_expired = False
            new_otp_ins.created_on = timezone.now()
            new_otp_ins.count += 1
        else:
            new_otp_ins = acc_models.PhoneOTP.objects.create(
                phone=phone, count=count)
        new_otp_ins.otp = generateUniqueOTP(new_otp_ins)
        new_otp_ins.save()
        otp_ins_to_send = new_otp_ins
    return otp_ins_to_send


def generate_random_digits(size=4, chars=string.digits):
    '''generates a random string of 6 digits'''
    import random
    return ''.join(random.choice(chars) for _ in range(size))


def generateUniqueOTP(instance, newOTP=None):
    """
        This is for a Django project and it assumes your instance
        has a model with a  field.
    """
    if newOTP is not None:
        OTP = newOTP
    else:
        '''First the flow comes here when a new OTP
            is created so generates an OTP of length 6'''
        OTP = generate_random_digits(size=6)

    '''Grabs the instance class'''
    Klass = instance.__class__
    qs = Klass.objects.filter(otp=OTP)
    if qs.exists():
        '''If OTP exists, it generates a brand new one but it doesn't\
            guarantte a unique one '''
        newOTP = generate_random_digits(size=6)
        '''So it is sent for unique test again and it continues untill it\
            finds a unique one '''
        return generateUniqueOTP(instance, newOTP=newOTP)
    '''Finally return OTP if found a unique one'''
    return OTP