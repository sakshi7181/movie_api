from django.core.management.base import BaseCommand
from api.models import Movie
from django.contrib.auth.models import User

class Command(BaseCommand):
    help = 'Assign ownership for movies without owners'

    def handle(self, *args, **options):
        # Find unowned movies
        unowned_movies = Movie.objects.filter(created_by__isnull=True)
        self.stdout.write(self.style.SUCCESS(f"Found {unowned_movies.count()} unowned movies"))
        
        # Get user smita (ID: 3)
        try:
            user = User.objects.get(id=3)
            self.stdout.write(f"Assigning to user: {user.username}")
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR("User with ID 3 not found"))
            return
        
        # Assign ownership
        for movie in unowned_movies:
            movie.created_by = user
            movie.save()
            self.stdout.write(f"Updated movie {movie.id}: {movie.title}")
        
        # Verify
        self.stdout.write(self.style.SUCCESS(f"All done! Updated {unowned_movies.count()} movies"))
        self.stdout.write("\nCurrent movie ownership:")
        for movie in Movie.objects.all():
            owner = "None" if movie.created_by is None else f"{movie.created_by.username} (ID: {movie.created_by.id})"
            self.stdout.write(f"Movie {movie.id}: {movie.title} - Owner: {owner}")