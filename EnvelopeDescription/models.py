from django.db import models
from django.db.models import Q
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

# Create your models here.
class EnvelopeDescription(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)  # linked to username indirectly
    EnvelopeName = models.ForeignKey('Envelopes.Envelope_Home', on_delete=models.CASCADE)  # Limits to current user
    Description = models.TextField()
    Money_Spent = models.DecimalField(max_digits=10, decimal_places=2)
    Money_Remaining = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(Money_Spent__gt=0), name='envdesc_spent_gt_0'),
        ]

    def clean(self):
        errors = {}
        if self.Money_Spent is None or self.Money_Spent <= 0:
            errors['Money_Spent'] = "Money spent must be greater than 0."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        self.full_clean()
        return super().save(*args, **kwargs)


