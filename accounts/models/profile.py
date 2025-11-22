from ckeditor.fields import RichTextField
from smart_selects.db_fields import ChainedForeignKey
from django.db.models.signals import post_save
from django.dispatch import receiver
from .user import User
from .location import *


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    birth_date = models.DateField(null=True, blank=True)
    bio = RichTextField()
    status = models.CharField(max_length=30, blank=True)
    score = models.IntegerField(default=0)
    location_region = models.ForeignKey("Region", on_delete=models.CASCADE, null=True, blank=True)
    location_district = models.ForeignKey("District", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    user = instance

    if created and user.is_active:
        Profile.objects.get_or_create(
            user=user,
            bio="this is my bio",
            age=user.age

        )


