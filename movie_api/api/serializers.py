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
    created_by_id = serializers.SerializerMethodField()
    owner_id = serializers.SerializerMethodField()  # Alternative field name for ownership checks
    is_owner = serializers.SerializerMethodField()  # Direct boolean check

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'genre', 'poster', 
                 'created_by_username', 'created_by_id', 'owner_id', 'is_owner']
    
    def get_created_by_username(self, obj):
        if obj.created_by:
            return obj.created_by.username
        return None
        
    def get_created_by_id(self, obj):
        if obj.created_by:
            return obj.created_by.id
        return None
        
    def get_owner_id(self, obj):
        # Alternative field name that might be easier to check in the frontend
        if obj.created_by:
            return obj.created_by.id
        return None
        
    def get_is_owner(self, obj):
        # Direct check if the requesting user is the owner
        request = self.context.get('request')
        
        # Add debug info
        auth_status = "No request in context"
        if request:
            auth_status = f"User authenticated: {request.user.is_authenticated}"
            if request.user.is_authenticated:
                auth_status += f", User ID: {request.user.id}, Username: {request.user.username}"
        
        print(f"DEBUG - Movie {obj.id} ({obj.title}) ownership check: {auth_status}")
        
        if request and request.user.is_authenticated and obj.created_by:
            is_owner = request.user.id == obj.created_by.id
            print(f"DEBUG - Movie {obj.id}: User {request.user.id} vs Created by {obj.created_by.id}, is_owner={is_owner}")
            return is_owner
        return False
