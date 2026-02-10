from django.contrib.auth import get_user_model
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from accounts.models.profile import Profile

User = get_user_model()


from rest_framework import serializers


class LoginSerializer(serializers.Serializer):
    phone = serializers.CharField()
    password = serializers.CharField(write_only=True)
    def validate(self, attrs):
        phone = attrs.get("phone")
        password = attrs.get("password")

        try:
            user = User.objects.get(phone=phone)
        except User.DoesNotExist:
            raise serializers.ValidationError("Telefon yoki parol noto‘g‘ri")

        if not user.check_password(password):
            raise serializers.ValidationError("Telefon yoki parol noto‘g‘ri")

        if not user.is_active:
            raise serializers.ValidationError("Foydalanuvchi faol emas")

        # 🔑 MUHIM
        attrs["user"] = user
        return attrs


class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()



class CustomUserSerializer(serializers.ModelSerializer):
    username = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    age = serializers.CharField(required=True)
    phone = serializers.CharField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(required=True, write_only=True, validators=[validate_password])
    password2 = serializers.CharField(required=True, write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'age', 'phone', 'password', 'password2','email']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "The passwords do not match.!"})
        return attrs

    def create(self, validated_data):
        validated_data.pop("password2")

        password = validated_data.pop("password")

        user = User.objects.create_user(password=password, **validated_data)
        return user


class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = "__all__"
        read_only_fields = ['user', 'score']


class UserDetailModelSerializer(serializers.ModelSerializer):
    class Meta:
        model=User
        fields=['username',"phone","age","email"]


class RatingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    rank = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['rank', 'username', 'score']

    def get_rank(self, obj):
        # Serializer context orqali obyektlar ro‘yxatini olish
        ranked_profiles = self.context.get('ranked_profiles', [])
        for index, profile in enumerate(ranked_profiles, start=1):
            if profile.id == obj.id:
                return index
        return None




class RatingSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username')
    rank = serializers.SerializerMethodField()

    class Meta:
        model = Profile
        fields = ['rank', 'username', 'score']

    def get_rank(self, obj):
        ranked_profiles = self.context.get('ranked_profiles', [])
        for index, profile in enumerate(ranked_profiles, start=1):
            if profile.id == obj.id:
                return index
        return None
