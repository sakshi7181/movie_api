from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Movie

class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 'last_name']
    
    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            email=validated_data.get('email', ''),
            first_name=validated_data.get('first_name', ''),
            last_name=validated_data.get('last_name', '')
        )
        return user

class MovieSerializer(serializers.ModelSerializer):
    poster = serializers.ImageField(use_url=True, required=False, allow_null=True)
    created_by_username = serializers.SerializerMethodField()

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'genre', 'poster', 'created_by_username']
    
    def get_created_by_username(self, obj):
        if obj.created_by:
            return obj.created_by.username
        return None
