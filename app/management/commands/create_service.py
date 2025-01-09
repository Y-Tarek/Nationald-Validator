from django.core.management import BaseCommand
from app.models import Service
from app.utility import sign_request

class Command(BaseCommand):
    help = "Create Service and an ecrypted private key printed for usage."

    def handle(self, *args, **options):
        s, created = Service.objects.get_or_create(
            service_name = "Shahry Service"
        )
        if created:
           print("New service Created")

        print(f"Public Key:{s.public_key}")
        print("--------------------------------------------------------------------------------------------------------------------")
        print(f"a signed provate key: {sign_request(s.private_key)}")
        