from django.contrib import admin
from .models import *


# Register your models here.

@admin.register(Vocab)
class VocabAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'image',
        'word_1',
        'word_uz',
        'text_1',
        'text_uz',
        'audio',

    )


@admin.register(Language)
class LanguageAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'name'
    )


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'created_at',
        'name',
        'description',

    )


@admin.register(BookProgress)
class BookAdmin(admin.ModelAdmin):
    list_display = (
        'id',
        'user',
        'book',
        'last_page'

    )
