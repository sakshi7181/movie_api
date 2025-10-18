from django.core.management.base import BaseCommand
from api.models import Movie
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Check movie ownership data'

    def handle(self, *args, **options):
        # Count total movies
        self.stdout.write(self.style.SUCCESS(f"Total movies in database: {Movie.objects.count()}"))

        # List all movies with their owners
        self.stdout.write("\nMovie ownership details:")
        for movie in Movie.objects.all():
            owner = "None" if movie.created_by is None else f"{movie.created_by.username} (ID: {movie.created_by.id})"
            self.stdout.write(f"Movie ID {movie.id}: {movie.title} - Owner: {owner}")

        # List all users
        self.stdout.write("\nUsers in system:")
        for user in User.objects.all():
            self.stdout.write(f"User ID {user.id}: {user.username}")

        # Count movies without owners
        no_owner_count = Movie.objects.filter(created_by__isnull=True).count()
        self.stdout.write(self.style.WARNING(f"\nMovies without owner: {no_owner_count}"))