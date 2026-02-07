from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class Income_Table(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    IncomeName = models.CharField(max_length=200)
    Total_Amount = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    Created_At = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.IncomeName


class Income_Description(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    IncomeName = models.ForeignKey('Income.Income_Table', on_delete=models.CASCADE)
    Description = models.TextField(blank=True)
    Amount = models.DecimalField(max_digits=12, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)

    def clean(self):
        errors = {}
        if self.Amount is None or self.Amount <= 0:
            errors['Amount'] = "Amount must be greater than 0."
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        # On create/update, adjust the parent Income_Table Total_Amount
        is_update = self.pk is not None
        previous_amount = 0
        if is_update:
            try:
                old = Income_Description.objects.get(pk=self.pk)
                previous_amount = old.Amount
            except Income_Description.DoesNotExist:
                previous_amount = 0

        self.full_clean()
        super().save(*args, **kwargs)

        # Adjust related Income_Table total
        try:
            income = Income_Table.objects.get(id=self.IncomeName.id)
            # compute delta and update
            delta = self.Amount - previous_amount
            income.Total_Amount = (income.Total_Amount or 0) + delta
            income.save()
        except Income_Table.DoesNotExist:
            pass

    def delete(self, *args, **kwargs):
        # On delete, subtract this amount from parent Total_Amount
        try:
            income = Income_Table.objects.get(id=self.IncomeName.id)
            income.Total_Amount = max(0, (income.Total_Amount or 0) - (self.Amount or 0))
            income.save()
        except Income_Table.DoesNotExist:
            pass
        return super().delete(*args, **kwargs)
