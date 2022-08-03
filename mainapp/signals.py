from django.db.models.signals import post_save
from django.contrib.auth.models import User
from .models import Profile

def Profile_signals(sender,instance,created,**kwargs):
    if created:
        Profile.objects.create(
            user = instance,
            first_name = instance.first_name,
            last_name = instance.last_name,
            email = instance.email
        )

post_save.connect(Profile_signals,sender=User)