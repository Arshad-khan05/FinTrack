from django.db import models
from django.db.models import F, Q
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Envelope_Home(models.Model):
    # Create your models here.
    username = models.ForeignKey(User, on_delete=models.CASCADE)  # linked to username indirectly
    Envelope_Name = models.CharField(max_length=200)
    Money_Allocated = models.IntegerField()
    Money_Remaining = models.IntegerField()
    Money_Spent = models.IntegerField()
    Created_At = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.CheckConstraint(check=Q(Money_Allocated__gte=0), name='env_allocated_gte_0'),
            models.CheckConstraint(check=Q(Money_Spent__gte=0), name='env_spent_gte_0'),
            models.CheckConstraint(
                check=Q(Money_Remaining=F('Money_Allocated') - F('Money_Spent')),
                name='env_remaining_consistent'
            ),
        ]

    def clean(self):
        errors = {}
        if self.Money_Allocated is None or self.Money_Allocated < 0:
            errors['Money_Allocated'] = "Money allocated cannot be negative."
        if self.Money_Spent is None or self.Money_Spent < 0:
            errors['Money_Spent'] = "Money spent cannot be negative."
        if self.Money_Allocated is not None and self.Money_Spent is not None:
            if self.Money_Remaining is not None:
                expected_remaining = self.Money_Allocated - self.Money_Spent
                if self.Money_Remaining != expected_remaining:
                    errors['Money_Remaining'] = "Money remaining must equal money allocated minus money spent."

        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        if self.Money_Allocated is not None and self.Money_Spent is not None:
            self.Money_Remaining = self.Money_Allocated - self.Money_Spent
        self.full_clean()
        return super().save(*args, **kwargs)

    def __str__(self):
        return self.Envelope_Name 