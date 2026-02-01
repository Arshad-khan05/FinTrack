from django.core.management.base import BaseCommand
from django.core.mail import send_mail
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from datetime import timedelta
from Envelopes.models import Envelope_Home
from EnvelopeDescription.models import EnvelopeDescription


class Command(BaseCommand):
    help = "Send monthly spending report emails to all users"

    def handle(self, *args, **kwargs):
        now = timezone.now()
        
        # Calculate previous month
        first_of_current_month = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0)
        last_of_previous_month = first_of_current_month - timedelta(days=1)
        previous_month = last_of_previous_month.month
        previous_year = last_of_previous_month.year
        
        # Get all users
        users = User.objects.all()
        
        for user in users:
            self.send_monthly_report(user, previous_month, previous_year)
        
        self.stdout.write(self.style.SUCCESS(f"Monthly spending reports sent to {users.count()} users"))

    def send_monthly_report(self, user, month, year):
        """Generate and send monthly spending report for a specific user"""
        
        # Get user's envelopes
        envelopes = Envelope_Home.objects.filter(username=user)
        
        if not envelopes.exists():
            return  # Skip users with no envelopes
        
        # Get previous month's transactions
        transactions = EnvelopeDescription.objects.filter(
            username=user,
            created_at__month=month,
            created_at__year=year
        ).order_by('EnvelopeName', 'created_at')
        
        # Generate report content
        subject = f"FinTrack Monthly Spending Report - {self.get_month_name(month)} {year}"
        message = self.generate_email_content(user, envelopes, transactions, month, year)
        
        # Send email
        try:
            send_mail(
                subject=subject,
                message=message,
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@fintrack.com',
                recipient_list=[user.email],
                fail_silently=False,
            )
            self.stdout.write(self.style.SUCCESS(f"Report sent to {user.username} ({user.email})"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to send email to {user.username}: {str(e)}"))

    def generate_email_content(self, user, envelopes, transactions, month, year):
        """Generate the email message content"""
        
        month_name = self.get_month_name(month)
        
        message = f"Hi {user.username},\n\n"
        message += f"Here's your spending report for {month_name} {year}:\n\n"
        message += "=" * 70 + "\n"
        message += "ENVELOPE SUMMARY\n"
        message += "=" * 70 + "\n\n"
        
        # Analyze each envelope
        overspent_envelopes = []
        well_spent_envelopes = []
        exact_spent_envelopes = []
        
        for envelope in envelopes:
            envelope_name = envelope.Envelope_Name
            allocated = envelope.Money_Allocated
            spent = envelope.Money_Spent
            remaining = envelope.Money_Remaining
            
            # Categorize spending status
            if remaining < 0:
                status = "OVERSPENT"
                overspent_envelopes.append(envelope_name)
            elif spent == allocated:
                status = "SPENT EXACTLY"
                exact_spent_envelopes.append(envelope_name)
            else:
                status = "WITHIN BUDGET"
                well_spent_envelopes.append(envelope_name)
            
            message += f"📁 {envelope_name}\n"
            message += f"   Allocated: ₹{allocated}\n"
            message += f"   Spent: ₹{spent}\n"
            message += f"   Remaining: ₹{remaining}\n"
            message += f"   Status: {status}\n\n"
        
        # Summary section
        message += "=" * 70 + "\n"
        message += "SPENDING ANALYSIS\n"
        message += "=" * 70 + "\n\n"
        
        if overspent_envelopes:
            message += f"⚠️  OVERSPENT ({len(overspent_envelopes)}): {', '.join(overspent_envelopes)}\n\n"
        
        if exact_spent_envelopes:
            message += f"✅ SPENT EXACTLY ({len(exact_spent_envelopes)}): {', '.join(exact_spent_envelopes)}\n\n"
        
        if well_spent_envelopes:
            message += f"✓  WITHIN BUDGET ({len(well_spent_envelopes)}): {', '.join(well_spent_envelopes)}\n\n"
        
        # Transaction history
        if transactions.exists():
            message += "=" * 70 + "\n"
            message += f"TRANSACTION HISTORY ({transactions.count()} transactions)\n"
            message += "=" * 70 + "\n\n"
            
            current_envelope = None
            for transaction in transactions:
                envelope_name = transaction.EnvelopeName.Envelope_Name
                
                # Group by envelope
                if current_envelope != envelope_name:
                    if current_envelope is not None:
                        message += "\n"
                    message += f"--- {envelope_name} ---\n"
                    current_envelope = envelope_name
                
                date_str = transaction.created_at.strftime("%b %d, %Y %I:%M %p")
                message += f"  • {date_str}\n"
                message += f"    Description: {transaction.Description}\n"
                message += f"    Amount Spent: ₹{transaction.Money_Spent}\n"
                message += f"    Balance After: ₹{transaction.Money_Remaining}\n\n"
        else:
            message += "=" * 70 + "\n"
            message += "No transactions recorded for this month.\n"
            message += "=" * 70 + "\n\n"
        
        message += "\n" + "=" * 70 + "\n"
        message += "This is an automated monthly report from FinTrack.\n"
        message += "Keep tracking your spending and stay within your budget!\n"
        message += "=" * 70 + "\n"
        
        return message

    def get_month_name(self, month):
        """Convert month number to month name"""
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        return months[month - 1]
