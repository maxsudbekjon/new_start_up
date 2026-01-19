from rest_framework import serializers
from task.models import Task
from vocab.models.book import Book
from vocab.models.vocab import Vocab








class TaskSerializer(serializers.ModelSerializer):
    book = serializers.CharField(source="book.name", read_only=True)

    class Meta:
        model = Task
        fields = ["title", "program", "count", "book"]

        read_only_fields = ['user']

    @staticmethod
    def _is_book_reading(title):
        normalized = (title or "").strip().lower()
        return normalized in {"kitob o'qish", "kitob oqish"}

    def create(self, validated_data):
        title_obj = validated_data.get("title")
        if title_obj and self._is_book_reading(title_obj.title):
            book = Book.objects.order_by("id").first()
            if not book:
                raise serializers.ValidationError({"book": "Kitob topilmadi, avval kitob qo'shing."})
            validated_data["book"] = book
        return super().create(validated_data)

    def update(self, instance, validated_data):
        instance = super().update(instance, validated_data)
        if self._is_book_reading(instance.title.title):
            if not instance.book:
                book = Book.objects.order_by("id").first()
                if not book:
                    raise serializers.ValidationError({"book": "Kitob topilmadi, avval kitob qo'shing."})
                instance.book = book
                instance.save(update_fields=["book"])
        elif instance.book_id is not None:
            instance.book = None
            instance.save(update_fields=["book"])
        return instance

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
            "is_active"
    
        ]


class VocabSerializer(serializers.ModelSerializer):
    class Meta:
        model = Vocab
        fields = ['id', "image", 'word_1', "word_uz", "text_1", "text_uz", "audio", "language"]


class ComplatetasTimeSerializer(serializers.Serializer):
    start_time=serializers.TimeField()
    end_time=serializers.TimeField()
    
