from django.conf import settings
from django.core.management.base import BaseCommand
from users.models import User


class Command(BaseCommand):

    def handle(self, *args, **options):
        if User.objects.count() == 0:
            username = settings.DEFAULT_ADMIN[0].replace(' ', '')
            email = settings.DEFAULT_ADMIN[1]
            password = 'admin'
            print('Creating user for %s (%s)' % (username, email))
            admin = User.objects.create_superuser(email=email,
                                                  username=username,
                                                  password=password)
            admin.is_active = True
            admin.is_admin = True
            admin.save()
        else:
            print('Admin user can only be initialized if no Users exist')
