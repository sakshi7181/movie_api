from django.core.management.base import BaseCommand
from api.models import Movie
from django.contrib.auth.models import User
from django.db import transaction

class Command(BaseCommand):
    help = 'Fix movie ownership by assigning unowned movies to a user'

    def add_arguments(self, parser):
        parser.add_argument('user_id', type=int, help='User ID to assign movies to')

    def handle(self, *args, **options):
        user_id = options['user_id']
        
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            self.stdout.write(self.style.ERROR(f"User with ID {user_id} does not exist"))
            return
            
        self.stdout.write(f"Assigning unowned movies to user: {user.username} (ID: {user.id})")
        
        # Get count of unowned movies
        unowned_count = Movie.objects.filter(created_by__isnull=True).count()
        self.stdout.write(f"Found {unowned_count} unowned movies")
        
        if unowned_count == 0:
            self.stdout.write(self.style.SUCCESS("No unowned movies to fix"))
            return
            
        # Assign all unowned movies to the specified user
        with transaction.atomic():
            updated = Movie.objects.filter(created_by__isnull=True).update(created_by=user)
            self.stdout.write(self.style.SUCCESS(f"Successfully assigned {updated} movies to {user.username}"))
            
        # Final check
        remaining_unowned = Movie.objects.filter(created_by__isnull=True).count()
        if remaining_unowned > 0:
            self.stdout.write(self.style.WARNING(f"Warning: {remaining_unowned} movies still have no owner"))