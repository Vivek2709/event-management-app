from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Event(models.Model): 
    id = models.AutoField(primary_key=True)
    title = models.CharField(unique=True, max_length=100)
    description = models.TextField(max_length=500)
    event_date = models.DateField()
    location = models.CharField(max_length=200)
    organizer = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.title}"

class Attendee(models.Model):
    id = models.AutoField(primary_key=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField()
    contact_number = models.CharField(max_length=10)

    class Meta:
        unique_together = ('event','email')

    def __str__(self):
        return f"{self.name}"