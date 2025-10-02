from rest_framework import serializers
from task.models import Task
from vocab.models.vocab import Vocab








class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["title","program","count"]

        read_only_fields = ['user']


class ListTaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="title.title", read_only=True)
    program = serializers.CharField(source="program.title", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "program",
            "count",
            "is_active",
        ]


class VocabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocab
        fields = ['id', "image", 'word_1', "word_uz", "text_1", "text_uz", "audio", "language"]


class ComplatetasTimeSerializer(serializers.Serializer):
    start_time=serializers.TimeField()
    end_time=serializers.TimeField()
    