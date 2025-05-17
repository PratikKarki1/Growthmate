from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.db import transaction
from django.core.management import CommandError
from growth_mate_app.models import UserProfile

class Command(BaseCommand):
    help = 'Creates a superuser with email, first name, last name, and admin role'

    def add_arguments(self, parser):
        parser.add_argument('--username', help='Username for the superuser')
        parser.add_argument('--email', help='Email for the superuser')
        parser.add_argument('--first_name', help='First name for the superuser')
        parser.add_argument('--last_name', help='Last name for the superuser')
        parser.add_argument('--noinput', '--no-input', action='store_false', dest='interactive',
                          help='Tells Django to NOT prompt the user for input of any kind.')

    def get_input_data(self, field_name, prompt, password=False):
        """Get input data from the user."""
        if password:
            import getpass
            return getpass.getpass(prompt)
        return input(prompt)

    def handle(self, *args, **options):
        User = get_user_model()
        username = options.get('username')
        email = options.get('email')
        first_name = options.get('first_name')
        last_name = options.get('last_name')
        interactive = options.get('interactive', True)

        # Validate that we have all required fields
        if not username and interactive:
            username = self.get_input_data('username', 'Username: ')
        if not email and interactive:
            email = self.get_input_data('email', 'Email address: ')
        if not first_name and interactive:
            first_name = self.get_input_data('first_name', 'First name: ')
        if not last_name and interactive:
            last_name = self.get_input_data('last_name', 'Last name: ')

        if not username or not email:
            raise CommandError('Username and email are required.')

        # Check if the user already exists
        if User.objects.filter(username=username).exists():
            raise CommandError('That username is already taken.')
        if User.objects.filter(email=email).exists():
            raise CommandError('That email is already taken.')

        # Get password
        password = None
        if interactive:
            password = self.get_input_data('password', 'Password: ', password=True)
            while not password:
                password = self.get_input_data('password', 'Password: ', password=True)
            password_confirm = self.get_input_data('password (again)', 'Password (again): ', password=True)
            while password != password_confirm:
                self.stdout.write(self.style.ERROR('Error: Your passwords did not match.'))
                password = self.get_input_data('password', 'Password: ', password=True)
                password_confirm = self.get_input_data('password (again)', 'Password (again): ', password=True)
        else:
            # Generate a random password
            from django.contrib.auth.hashers import make_password
            import secrets
            password = secrets.token_urlsafe(10)
            self.stdout.write(self.style.WARNING(f'Generated password: {password}'))

        try:
            with transaction.atomic():
                # Create the superuser
                user = User.objects.create_superuser(
                    username=username,
                    email=email,
                    password=password,
                    first_name=first_name,
                    last_name=last_name
                )
                
                # Update or create UserProfile with admin role
                UserProfile.objects.update_or_create(
                    user=user,
                    defaults={'role': 'admin'}
                )
                
                self.stdout.write(self.style.SUCCESS(f'Superuser "{username}" was created successfully with admin role.'))
        except Exception as e:
            raise CommandError(str(e))