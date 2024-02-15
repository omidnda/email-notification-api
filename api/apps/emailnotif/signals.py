from django.db.models.signals import post_save
from django.dispatch import receiver
from utils import send_email
from .models import Newsletter, CustomUser
from rest_framework.authtoken.models import Token

@receiver(post_save, sender=Newsletter)
def send_newsletter(sender, instance, **kwargs):
        users = CustomUser.objects.filter(subscribed_newletter=True)
        if instance.is_active==True:
            for user in users:
                send_email(instance.subject,instance.content,user,)
            
           
