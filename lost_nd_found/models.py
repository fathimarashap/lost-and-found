from django.db import models

# Create your models here.

from django.db import models

from django.db import models

from cloudinary.models import CloudinaryField   


class UserTable(models.Model):
    name = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    pin = models.CharField(max_length=10)
    username = models.CharField(max_length=100)
    image = CloudinaryField('image', blank=True, null=True)
    phone = models.CharField(max_length=15)
    email = models.EmailField()
    password = models.CharField(max_length=100)
    is_admin =models.BooleanField(default=False)

class ItemTable(models.Model):
    userid = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    image = CloudinaryField('image', blank=True, null=True)
    details = models.TextField()
    date = models.DateField()
    status = models.CharField(max_length=50)

class Complaints(models.Model):
    userid = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    complaint = models.TextField()
    date = models.DateField()
    reply = models.TextField(blank=True, null=True)

class Found(models.Model):
    userid = models.ForeignKey(UserTable, on_delete=models.CASCADE)
    item = models.ForeignKey(ItemTable, on_delete=models.CASCADE)
    image = CloudinaryField('image', blank=True, null=True)
    details = models.TextField()
    date = models.DateField()
    status = models.CharField(max_length=50)
