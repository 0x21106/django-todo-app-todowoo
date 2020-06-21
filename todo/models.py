from django.db import models
from django.contrib.auth.models import User
from colorfield.fields import ColorField

# Create your models here.
class Status(models.Model):
    name = models.CharField(max_length=50)
    def __str__(self):
        return self.name

class Materiality(models.Model):
    name = models.CharField(max_length=50)
    color = ColorField(default='#4FE152', blank = True)
    def __str__(self):
        return self.name

class Todo(models.Model):
    title = models.CharField(max_length=100)
    note = models.TextField(blank=True)
    # status = models.IntegerField(default=1, blank=True)
    status = models.ForeignKey(Status, on_delete = models.CASCADE)
    # materiality = models.IntegerField(default=1, blank=True)
    materiality = models.ForeignKey(Materiality, on_delete = models.CASCADE)
    isActive = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add = True)
    lastModified = models.DateTimeField(auto_now = True)
    dateCompleted = models.DateTimeField(null = True, blank=True)
    user = models.ForeignKey(User, on_delete = models.CASCADE)

    def __str__(self):
        return f"{self.title}:{self.status} - {self.materiality} | {self.user.pk}:{self.user}"