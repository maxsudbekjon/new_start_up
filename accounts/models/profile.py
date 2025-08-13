from django.db import models
from ckeditor.fields import RichTextField
from smart_selects.db_fields import ChainedForeignKey

from .location import *

class Profile(models.Model):
    user = models.OneToOneField('User', on_delete=models.CASCADE)
    image = models.ImageField(default='default.jpg', upload_to='profile_pics')
    birth_date = models.DateField(null=True, blank=True)
    bio = RichTextField()
    status = models.CharField(max_length=30, blank=True)
    score = models.IntegerField(default=0)
    location_region = models.ForeignKey("Region", on_delete=models.CASCADE, null=True, blank=True)
    location_district = ChainedForeignKey("District", chained_field="location_region", chained_model_field="region", on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.user.username} Profile'
