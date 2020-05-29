import stripe
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.signals import user_logged_in
from django.db.models.signals import post_save
from .models import UserStripe, EmailConfirmed

User = get_user_model()
stripe.api_key = settings.STRIPE_SECRET_KEY


def get_create_stripe(user):
    new_user_stripe, created = UserStripe.objects.get_or_create(user=user)
    if created:
        customer = stripe.Customer.create(
            email = str(user.email)
        )
        new_user_stripe.stripe_id = customer.id
        new_user_stripe.save()

def user_created(sender, instance, created, *args, **kwargs):
    user = instance
    if created:
        get_create_stripe(user)
        email_confirmed, email_is_created = EmailConfirmed.objects.get_or_create(user=user)
        if email_is_created:
            pass
            # create hash
            # user.emailconfirmed.email_user()

post_save.connect(user_created, sender=User)



# OLD WAY OF ADDING STRIPE ID
# # example stripe id --> "id": "cus_HMhDIg0vlgYyuO",
# def get_or_create_stripe(sender, user, *args, **kwargs):
#     try:
#         user.userstripe.stripe_id
#     except UserStripe.DoesNotExist:
#         customer = stripe.Customer.create(
#             email=str(user.email)
#         )
#         new_user_stripe = UserStripe.objects.create(
#             user=user,
#             stripe_id=customer.id,
#         )
#     except:
#         pass
# user_logged_in.connect(get_or_create_stripe)