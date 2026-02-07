from django.core.management.base import BaseCommand
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from django.contrib.auth.models import User
from django.conf import settings
from datetime import timedelta
from Envelopes.models import Envelope_Home
from EnvelopeDescription.models import EnvelopeDescription
from Income.models import Income_Table, Income_Description


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
        html_message = self.generate_html_email_content(user, envelopes, transactions, month, year)
        text_message = f"Hi {user.username},\n\nYour monthly spending report for {self.get_month_name(month)} {year} is ready. Please open this email in an HTML-compatible email client to view the formatted report."
        
        # Send email with HTML
        try:
            email = EmailMultiAlternatives(
                subject=subject,
                body=text_message,
                from_email=settings.DEFAULT_FROM_EMAIL if hasattr(settings, 'DEFAULT_FROM_EMAIL') else 'noreply@fintrack.com',
                to=[user.email],
            )
            email.attach_alternative(html_message, "text/html")
            email.send(fail_silently=False)
            self.stdout.write(self.style.SUCCESS(f"Report sent to {user.username} ({user.email})"))
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to send email to {user.username}: {str(e)}"))

    def generate_html_email_content(self, user, envelopes, transactions, month, year):
        """Generate the HTML email message content"""
        
        month_name = self.get_month_name(month)
        user_name = user.first_name or user.username
        
        # Analyze each envelope
        overspent_envelopes = []
        well_spent_envelopes = []
        exact_spent_envelopes = []
        envelope_data = []
        
        for envelope in envelopes:
            envelope_name = envelope.Envelope_Name
            allocated = envelope.Money_Allocated
            spent = envelope.Money_Spent
            remaining = envelope.Money_Remaining
            
            if remaining < 0:
                status = "OVERSPENT"
                status_color = "#ff4444"
                status_badge = "🔴 Overspent"
                overspent_envelopes.append(envelope_name)
            elif spent == allocated:
                status = "SPENT EXACTLY"
                status_color = "#ffaa00"
                status_badge = "🟡 Exact"
                exact_spent_envelopes.append(envelope_name)
            else:
                status = "WITHIN BUDGET"
                status_color = "#22cc44"
                status_badge = "🟢 Good"
                well_spent_envelopes.append(envelope_name)
            
            envelope_data.append({
                'name': envelope_name,
                'allocated': allocated,
                'spent': spent,
                'remaining': remaining,
                'status': status_badge,
                'color': status_color
            })
        
        # Start HTML
        html = f"""
        <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <style>
                body {{ font-family: Arial, sans-serif; color: #333; background-color: #f5f5f5; margin: 0; padding: 0; }}
                .container {{ max-width: 700px; margin: 20px auto; background-color: white; padding: 30px; border-radius: 8px; box-shadow: 0 2px 4px rgba(0,0,0,0.1); }}
                h1 {{ color: #2c3e50; border-bottom: 3px solid #3498db; padding-bottom: 10px; margin-top: 0; }}
                h2 {{ color: #34495e; margin-top: 25px; margin-bottom: 15px; }}
                .greeting {{ font-size: 16px; margin-bottom: 20px; }}
                table {{ width: 100%; border-collapse: collapse; margin-bottom: 20px; }}
                th {{ background-color: #3498db; color: white; padding: 12px; text-align: left; font-weight: bold; font-size: 13px; }}
                td {{ padding: 10px 12px; border-bottom: 1px solid #ecf0f1; font-size: 14px; }}
                tr:hover {{ background-color: #f9f9f9; }}
                .status-cell {{ font-weight: bold; padding: 6px 8px; border-radius: 4px; color: white; font-size: 12px; white-space: nowrap; display: inline-block; }}
                .summary-box {{ padding: 15px; border-left: 4px solid #3498db; background-color: #ecf0f1; margin: 15px 0; border-radius: 4px; font-size: 14px; }}
                .overspent {{ background-color: #ffebee; border-left-color: #ff4444; }}
                .within-budget {{ background-color: #e8f5e9; border-left-color: #22cc44; }}
                .exact-spent {{ background-color: #fff3e0; border-left-color: #ffaa00; }}
                .transaction-group {{ margin-bottom: 20px; }}
                .transaction-group h4 {{ margin: 10px 0 5px 0; color: #2c3e50; font-size: 14px; }}
                .transaction-item {{ padding: 10px; margin: 8px 0; background-color: #f9f9f9; border-left: 3px solid #3498db; border-radius: 3px; font-size: 13px; }}
                .transaction-date {{ font-weight: bold; color: #3498db; }}
                .transaction-desc {{ color: #555; margin: 5px 0; }}
                .transaction-amount {{ color: #e74c3c; font-weight: bold; }}
                .footer {{ text-align: center; margin-top: 30px; padding-top: 20px; border-top: 1px solid #ecf0f1; color: #7f8c8d; font-size: 12px; }}
                .money {{ color: #27ae60; font-weight: bold; }}
                @media only screen and (max-width: 600px) {{
                    .container {{ padding: 15px; margin: 10px; }}
                    table {{ font-size: 12px; }}
                    th, td {{ padding: 8px; }}
                    .status-cell {{ padding: 4px 6px; font-size: 11px; }}
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>💰 FinTrack Monthly Spending Report</h1>
                <p class="greeting">Hi <strong>{user_name}</strong>,</p>
                <p>Here's your detailed spending report for <strong>{month_name} {year}</strong>:</p>
                
                <h2>📊 Envelope Summary</h2>
                <table>
                    <thead>
                        <tr>
                            <th>Envelope</th>
                            <th>Allocated</th>
                            <th>Spent</th>
                            <th>Remaining</th>
                            <th>Status</th>
                        </tr>
                    </thead>
                    <tbody>
        """

        # Get income entries for the month
        incomes = Income_Description.objects.filter(
            username=user,
            created_at__month=month,
            created_at__year=year
        ).order_by('IncomeName', 'created_at')

        # Build income summary data
        income_groups = {}
        for inc in incomes:
            key = inc.IncomeName.IncomeName
            income_groups.setdefault(key, []).append(inc)

        
        # Add envelope rows
        for env in envelope_data:
            html += f"""
                        <tr>
                            <td>{env['name']}</td>
                            <td class="money">₹{env['allocated']}</td>
                            <td class="money">₹{env['spent']}</td>
                            <td class="money" style="color: {'#e74c3c' if env['remaining'] < 0 else '#27ae60'};">₹{env['remaining']}</td>
                            <td><span class="status-cell" style="background-color: {env['color']};">{env['status']}</span></td>
                        </tr>
            """
        
        html += """
                    </tbody>
                </table>
                
                <h2>📈 Spending Analysis</h2>
        """
        
        # Spending analysis summaries
        if overspent_envelopes:
            html += f"""
                <div class="summary-box overspent">
                    <strong>⚠️ Overspent ({len(overspent_envelopes)}):</strong><br/>
                    {', '.join(overspent_envelopes)}
                </div>
            """
        
        if exact_spent_envelopes:
            html += f"""
                <div class="summary-box exact-spent">
                    <strong>✅ Spent Exactly ({len(exact_spent_envelopes)}):</strong><br/>
                    {', '.join(exact_spent_envelopes)}
                </div>
            """
        
        if well_spent_envelopes:
            html += f"""
                <div class="summary-box within-budget">
                    <strong>✓ Within Budget ({len(well_spent_envelopes)}):</strong><br/>
                    {', '.join(well_spent_envelopes)}
                </div>
            """
        
        # Transaction history
        if transactions.exists():
            html += f"""
                <h2>📝 Transaction History ({transactions.count()} transactions)</h2>
            """
            
            current_envelope = None
            for transaction in transactions:
                envelope_name = transaction.EnvelopeName.Envelope_Name
                
                # Group by envelope
                if current_envelope != envelope_name:
                    if current_envelope is not None:
                        html += "</div>"
                    html += f"""<div class="transaction-group">
                        <h4>📁 {envelope_name}</h4>
                    """
                    current_envelope = envelope_name
                
                date_str = transaction.created_at.strftime("%b %d, %Y at %I:%M %p")
                html += f"""
                    <div class="transaction-item">
                        <div class="transaction-date">📅 {date_str}</div>
                        <div class="transaction-desc"><strong>Description:</strong> {transaction.Description}</div>
                        <div class="transaction-amount">💸 Amount: ₹{transaction.Money_Spent}</div>
                        <div style="color: #27ae60;"><strong>Balance After:</strong> ₹{transaction.Money_Remaining}</div>
                    </div>
                """
            
            if current_envelope is not None:
                html += "</div>"
        else:
            html += """
                <div class="summary-box">
                    <strong>ℹ️ No Transactions</strong><br/>
                    No transactions recorded for this month.
                </div>
            """
        
        # Income section
        if incomes.exists():
            html += f"""
                <h2>💵 Income Summary ({incomes.count()} items)</h2>
            """
            for name, items in income_groups.items():
                html += f"""
                    <div class=\"transaction-group\">\n                        <h4>📁 {name}</h4>\n                """
                for it in items:
                    date_str = it.created_at.strftime("%b %d, %Y at %I:%M %p")
                    html += f"""
                        <div class=\"transaction-item\">\n                            <div class=\"transaction-date\">📅 {date_str}</div>\n                            <div class=\"transaction-desc\"><strong>Description:</strong> {it.Description}</div>\n                            <div class=\"transaction-amount\">➕ Amount: ₹{it.Amount}</div>\n                        </div>\n                    """
                html += "</div>"
        else:
            html += """
                <div class="summary-box">
                    <strong>ℹ️ No Income Records</strong><br/>
                    No incomes recorded for this month.
                </div>
            """

        html += """
                <div class="footer">
                    <p><strong>FinTrack</strong> - Your Personal Expense Tracker</p>
                    <p>This is an automated monthly report. Keep tracking your spending and stay within your budget!</p>
                    <p style="font-size: 11px; color: #999;">Do not reply to this email.</p>
                </div>
            </div>
        </body>
        </html>
        """
        
        return html

    def get_month_name(self, month):
        """Convert month number to month name"""
        months = [
            "January", "February", "March", "April", "May", "June",
            "July", "August", "September", "October", "November", "December"
        ]
        return months[month - 1]
