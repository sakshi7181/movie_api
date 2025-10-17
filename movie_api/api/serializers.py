from rest_framework import serializers
from .models import Movie

class MovieSerializer(serializers.ModelSerializer):
    poster = serializers.ImageField(use_url=True)

    class Meta:
        model = Movie
        fields = ['id', 'title', 'description', 'release_date', 'genre', 'poster']
