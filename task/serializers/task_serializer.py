from rest_framework import serializers
from task.models import Task
from task.models.task import Do, Program
from vocab.models.book import Book
from vocab.models.vocab import Vocab




class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["title", "program", "count", "book"]

        read_only_fields = ['user']

    

class TitleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Do
        fields = ["id", "title"]


class ProgramSerializer(serializers.ModelSerializer):
    class Meta:
        model = Program
        fields = ["id", "title", "image"]


class ListTaskSerializer(serializers.ModelSerializer):
    title = TitleSerializer(read_only=True)
    program = ProgramSerializer(read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "program",
            "count",
            "is_active",
            "is_complete",
        ]


class VocabSerializer(serializers.ModelSerializer):
    language = serializers.SerializerMethodField()

    class Meta:
        model = Vocab
        fields = ['id', "image", 'word_1', "word_uz", "text_1", "text_uz", "audio", "language"]

    def get_language(self, obj):
        # Vocab has no direct language field; use reverse relation if present.
        return list(obj.language_set.values_list("name", flat=True))


class ComplatetasTimeSerializer(serializers.Serializer):
    start_time=serializers.TimeField()
    end_time=serializers.TimeField()
    
