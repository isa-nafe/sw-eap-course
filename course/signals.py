from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import UserPayment

@receiver(post_save, sender=User)
def create_or_update_user_payment_profile(sender, instance, created, **kwargs):
    if created:
        UserPayment.objects.create(user=instance)
    else:
        # Ensure the payment profile exists and save it if the user is saved
        # This handles cases where users might have been created before this signal
        try:
            instance.payment_profile.save()
        except UserPayment.DoesNotExist:
            UserPayment.objects.create(user=instance) # Create if it somehow doesn't exist
