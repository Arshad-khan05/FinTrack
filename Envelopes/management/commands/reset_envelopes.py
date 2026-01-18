from django.core.management.base import BaseCommand
from django.utils import timezone
from django.db import transaction
from Envelopes.models import Envelope_Home

class Command(BaseCommand):
    help = "Reset all envelopes at the start of the month"

    def handle(self, *args, **kwargs):
        now = timezone.now()

        with transaction.atomic():
            envelopes = Envelope_Home.objects.all()

            for env in envelopes:
                env.Money_Spent = 0
                env.Money_Remaining = env.Money_Allocated
                env.Date = now
                env.save()

        self.stdout.write(self.style.SUCCESS("Monthly envelope reset completed"))
