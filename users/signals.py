from django.db.models.signals import post_save
from django.contrib.auth.models import User
from django.dispatch import receiver
from .models import Profile

@receiver(post_save, sender = User)
def create_profile(sender, instance, created, **kwargs):
    if created:
        is_teacher = getattr(instance, '_is_teacher', False)
        Profile.objects.create(user=instance, is_teacher=is_teacher)


@receiver(post_save, sender = User)
def save_profile(sender, instance, **kwargs):
    instance.profile.save()