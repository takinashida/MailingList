from django.core.management import BaseCommand

from users.models import User


class Command(BaseCommand):
    help="Create superuser with nickname 'admin' and password '86427531'"
    def handle(self, *args, **options):
        user, created=User.objects.get_or_create(username="admin", email="admin@example.com")
        user.set_password("86427531")
        user.is_staff=True
        user.is_superuser=True
        user.save()
        if created:
            self.stdout.write(self.style.SUCCESS(f'Successfully added new superuser: {user.username}'))
        else:
            self.stdout.write(self.style.SUCCESS(f'Superuser {user.username} already exist'))

