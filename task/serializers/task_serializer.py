from rest_framework import serializers
from task.models import Task
from vocab.models.book import Book
from vocab.models.vocab import Vocab








class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = ["title", "program", "count", "book"]

        read_only_fields = ['user']

    

class ListTaskSerializer(serializers.ModelSerializer):
    title = serializers.CharField(source="title.title", read_only=True)
    program = serializers.CharField(source="program.title", read_only=True)
    program_image = serializers.ImageField(source="program.image", read_only=True)

    class Meta:
        model = Task
        fields = [
            "id",
            "title",
            "program",
            "program_image",
            "count",
            "is_active",
            "is_complete"
    
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
    
