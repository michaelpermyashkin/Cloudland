from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail

from django.template.loader import render_to_string


class UserStripe(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return str(self.stripe_id)


class EmailConfirmed(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Email Confirmations"

    def __str__(self):
        return str(self.confirmed)

    def activate_user_email(self):
        subject = 'Activate your Email'
        activation_url = 'http://localhost:8000/accounts/activate/%s' % (self.activation_key)
        context = {
            'user_firstname': self.user.first_name,
            'activation_key': self.activation_key,
            'activation_url': activation_url,
        }
        message = render_to_string('accounts/activation_message.txt', context)
        from_email = settings.DEFAULT_FROM_EMAIL
        self.email_user(subject, message, from_email)

    def email_user(self, subject, message, from_email=None, **kwargs):
        send_mail(subject, message, from_email, [self.user.email], kwargs)
