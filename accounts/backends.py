# backends.py
from django.contrib.auth.backends import ModelBackend

class AllowInactiveModelBackend(ModelBackend):
    def user_can_authenticate(self, user):
        # Override this method to allow inactive users to authenticate
        # (so that authenticate() returns the user even if is_active is False)
        return True
