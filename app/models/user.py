# models.py
from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    phone = models.CharField(max_length=255,default="None")


class Csv(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    old_csv= models.FileField(upload_to='Upload/old_csv_file/', blank=True, null=True)
    # new_csv = models.FileField(upload_to='new_csv_file/', blank=True, null=True)
    File_description = models.TextField(default="None")  # Changed from CharField to TextField
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    id=models.CharField(max_length=50,primary_key=True,null=False,default="54")

    def __str__(self):
        return self.id