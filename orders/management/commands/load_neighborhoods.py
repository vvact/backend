from django.core.management.base import BaseCommand
from orders.models import Neighborhood

NEIGHBORHOODS = [
    "Westlands", "Kileleshwa", "Kilimani", "Lavington", "Karen", "Runda",
    "South B", "South C", "Embakasi", "Donholm", "Buruburu", "Komarock",
    "Kayole", "Utawala", "Lang'ata", "Ruaka", "Thome", "Kahawa", "Githurai",
    "Zimmerman", "Kasarani", "Roysambu", "Hurlingham", "Ngara", "Pangani",
    "Parklands", "Eastleigh", "Muthaiga", "Gigiri", "Highridge", "CBD",
    "Umoja", "Tassia", "Madaraka", "Makadara", "Ngong Road", "Adams Arcade"
]

class Command(BaseCommand):
    help = 'Load Nairobi neighborhoods into the database'

    def handle(self, *args, **options):
        count = 0
        for name in NEIGHBORHOODS:
            obj, created = Neighborhood.objects.get_or_create(name=name)
            if created:
                count += 1
        self.stdout.write(self.style.SUCCESS(f'Successfully loaded {count} neighborhoods.'))
