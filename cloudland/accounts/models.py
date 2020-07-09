from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.urls import reverse

from django.template.loader import render_to_string

from localflavor.us.us_states import US_STATES

class UserDefaultAddresses(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    shipping = models.ForeignKey("UserAddress", null=True, blank=True, on_delete=models.CASCADE)
    billing = models.ForeignKey("UserBillingAddress", null=True, blank=True, on_delete=models.CASCADE)

    def __str__(self):
        return str(self.user.username)
    

class UserAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    address2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120, choices=US_STATES)
    zipcode = models.CharField(max_length=120)
    shipping = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated = models.DateTimeField(auto_now=False, auto_now_add=True)

    class Meta:
        ordering = ['-updated', '-timestamp']

    def __str__(self):
        return self.get_address()

    def get_address(self):
        if self.address2:
            return '%s, %s, %s, %s, %s' % (self.address, self.address2, self.city, self.state, self.zipcode)
        else:
            return '%s, %s, %s, %s' % (self.address, self.city, self.state, self.zipcode)


class UserBillingAddress(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    address = models.CharField(max_length=120)
    address2 = models.CharField(max_length=120, null=True, blank=True)
    city = models.CharField(max_length=120)
    state = models.CharField(max_length=120, choices=US_STATES)
    zipcode = models.CharField(max_length=120)
    timestamp = models.DateTimeField(auto_now=True, auto_now_add=False)
    updated = models.DateTimeField(auto_now=False, auto_now_add=True)
    
    class Meta:
        ordering = ['-updated', '-timestamp']

    def __str__(self):
        return self.get_address()

    def get_address(self):
        if self.address2:
            return '%s, %s, %s, %s, %s' % (self.address, self.address2, self.city, self.state, self.zipcode)
        else:
            return '%s, %s, %s, %s' % (self.address, self.city, self.state, self.zipcode)



class UserStripe(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    stripe_id = models.CharField(max_length=120, null=True, blank=True)

    def __str__(self):
        return str(self.stripe_id)


class EmailConfirmed(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    activation_key = models.CharField(max_length=200)
    confirmed = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Email Confirmations"

    def __str__(self):
        return str(self.confirmed)

    def activate_user_email(self):
        subject = 'Activate your Email'
        activation_url = '%s%s' %(settings.SITE_URL, reverse('activation-view', args=[self.activation_key]))
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
