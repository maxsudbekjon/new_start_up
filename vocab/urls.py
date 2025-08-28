from vocab.views import *
from django.urls import path

from vocab.views.book_view import BookListAPIView, BookCreateAPIView
from vocab.views.language_view import LanguageCreateAPIView, LanguageListAPIView
from vocab.views.vocab_view import VocabListAPIView, VocabCreateAPIView

# from vocab.views import *

urlpatterns = [
    path('Book-list/', view=BookListAPIView.as_view()),
    path('Book-create/', view=BookCreateAPIView.as_view()),

    path("Vocab-list/", view=VocabListAPIView.as_view()),
    path("Vocab-create/", view=VocabCreateAPIView.as_view()),

    path('Language-create/', view=LanguageCreateAPIView.as_view()),
    path('Language-list/', view=LanguageListAPIView.as_view()),
]