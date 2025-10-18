from django.db import models

class Rating(models.Model):
    point = models.IntegerField()
    user_profile = models.ForeignKey('Profile', on_delete=models.CASCADE)
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)