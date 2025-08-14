from django.contrib import admin

from .models import Rating
from .models.user import *
from .models.profile import *

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'phone', 'is_active')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'image',
        'birth_date',
        'status'

                    )

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = (
        'id','point','user_profile'
    )

@admin.register(District)
class DistrictAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'region',
        'name'
    )

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'name'
    )