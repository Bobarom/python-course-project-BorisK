from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Tab, Comment, Favorite


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined']


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password'],
        )
        return user


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')

    class Meta:
        model = Comment
        fields = ['id', 'author', 'content', 'created_at']


class TabSerializer(serializers.ModelSerializer):
    author = serializers.ReadOnlyField(source='author.username')
    comments = CommentSerializer(many=True, read_only=True)
    favorite_count = serializers.SerializerMethodField()

    class Meta:
        model = Tab
        fields = [
            'id', 'author', 'title', 'artist', 'song',
            'tuning', 'difficulty', 'content', 'description',
            'created_at', 'updated_at', 'comments', 'favorite_count'
        ]

    def get_favorite_count(self, obj):
        return obj.favorited_by.count()


class FavoriteSerializer(serializers.ModelSerializer):
    tab = TabSerializer(read_only=True)

    class Meta:
        model = Favorite
        fields = ['id', 'tab', 'created_at']