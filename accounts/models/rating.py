from django.db import models

class Rating(models.Model):
    point = models.IntegerField()
    user_profile = models.ForeignKey('Profile', on_delete=models.CASCADE)