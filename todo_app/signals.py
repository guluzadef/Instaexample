from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from todo_app.models import Verification
from todo_app.tasks import send_verification_email
from threading import Thread
#
User = get_user_model()
#
@receiver(post_save, sender=User, dispatch_uid='create_token')
def create_token(**kwargs):
    instance = kwargs.get("instance")
    created = kwargs.get("created")
    if created:
        Verification.objects.create(
            user=instance

        )
@receiver(post_save, sender=Verification, dispatch_uid='send_mail_to_user ')
def send_mail_to_user(**kwargs):
    instance = kwargs.get("instance")
    created = kwargs.get("created")
    if created:
        link=f"http://localhost:8020/verify/{instance.token}/{instance.user.id}"
        background_job=Thread(target=send_verification_email,args=(instance.user.email,link))
        background_job.start()

