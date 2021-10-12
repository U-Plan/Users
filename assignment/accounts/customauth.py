from django.contrib.auth import get_user_model
from django.db.models import Q

my_user_model = get_user_model()


class CustomAuthBackend(object):

    def authenticate(self, request, username=None, password=None):
        try:
            user = my_user_model.objects.get(
                Q(phone=username) | Q(email=username))
            if user.check_password(password):
                return user
        except my_user_model.DoesNotExist:
            return None
        return None
