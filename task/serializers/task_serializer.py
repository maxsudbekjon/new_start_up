from rest_framework import serializers
from task.models import Task
from vocab.models.vocab import Vocab


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["title","program","count","duration"]

        read_only_fields = ['user']

class VocabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocab
        fields = ['id', "image", 'word_1', "word_uz", "text_1", "text_uz", "audio", "language"]


