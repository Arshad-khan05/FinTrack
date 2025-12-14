from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class EnvelopeDescription(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)  # linked to username indirectly
    EnvelopeName = models.ForeignKey('Envelopes.Envelope_Home', on_delete=models.CASCADE)  # Limits to current user
    Description = models.TextField()
    Money_Spent = models.IntegerField()
    Money_Remaining = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)


