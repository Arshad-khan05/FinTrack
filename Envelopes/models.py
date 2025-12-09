from django.db import models
from django.contrib.auth.models import User

class Envelope_Home(models.Model):
    # Create your models here.
    username = models.ForeignKey(User, on_delete=models.CASCADE)  # linked to username indirectly
    Envelope_Name = models.CharField(max_length=200)
    Money_Allocated = models.IntegerField()
    Money_Remaining = models.IntegerField()
    Money_Spent = models.IntegerField()
    Created_At = models.DateTimeField(auto_now_add=True)