from django.db import models

# Create your models here.
class clientDB(models.Model):
    Email = models.EmailField(max_length=50)
    Username = models.CharField(max_length=50)
    Password = models.CharField(max_length=50)