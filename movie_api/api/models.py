from django.db import models
# movie_api_backend/api/models.py
from django.db import models
from django.contrib.auth.models import User

class Movie(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    release_date = models.DateField()
    genre = models.CharField(max_length=100)
    poster = models.ImageField(upload_to='poster/', blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        db_table = 'movies_movie'
        managed = True

    def __str__(self):
        return self.title
# Create your models here.
