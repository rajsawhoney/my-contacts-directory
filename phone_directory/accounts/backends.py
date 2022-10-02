from .models import User


class PhoneAuthentication(object):
    def authenticate(self, request, username=None, password=None):
        try:
            user = User.objects.get(phone=username)
            if user.check_password(password):
                return user
            return None
        except ValueError:
            return None

    def get_user(self, id):
        try:
            return User.objects.get(id=id)
        except ValueError:
            return None