from django.core.management.base import BaseCommand
from django.db import connection
from cr_portal.models import UserProfile, College

class Command(BaseCommand):
    help = 'Fix invalid college IDs in UserProfile table'

    def handle(self, *args, **kwargs):
        with connection.cursor() as cursor:
            cursor.execute("""
                SELECT id, college_id
                FROM cr_portal_userprofile
                WHERE college_id NOT IN (SELECT id FROM cr_portal_college)
            """)
            invalid_entries = cursor.fetchall()

            if invalid_entries:
                self.stdout.write(self.style.WARNING('Found invalid college IDs:'))
                for entry in invalid_entries:
                    user_id, college_id = entry
                    self.stdout.write(f'UserProfile ID: {user_id}, Invalid College ID: {college_id}')

                # Optional: Fixing invalid entries
                valid_college = College.objects.first()  # Use a valid College ID
                UserProfile.objects.filter(college_id__in=[e[1] for e in invalid_entries]).update(college_id=valid_college.id)
                self.stdout.write(self.style.SUCCESS(f'Updated invalid entries to valid college ID: {valid_college.id}'))
            else:
                self.stdout.write(self.style.SUCCESS('No invalid college IDs found'))
