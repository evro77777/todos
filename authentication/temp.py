from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.conf import settings
import six


class TokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        print('timestamp=',timestamp)
        settings.configure()
        return six.text_type(user['pk'])+six.text_type(timestamp)+six.text_type(user['is_email_verified'])



user = {'name':'Roma', 'pk':12, 'is_email_verified':True}


print(six.text_type(user['pk'])+six.text_type(677781087)+six.text_type(user['is_email_verified']))
print(timestamp)