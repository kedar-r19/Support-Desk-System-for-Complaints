from tkinter import CASCADE
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    is_owner = models.BooleanField(default=True)
    is_agent = models.BooleanField(default=False)
    is_customer = models.BooleanField(default=False)

class Agent(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    

    def __str__(self):
        return self.user.username

class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class Complaint(models.Model):

    SOURCE_CHOICES=(
        ('email','E-mail'),
        ('call','Call'),
        ('ticket','Ticket')
    )

    store_name=models.CharField(max_length=20)
    store_contact_no=models.IntegerField(max_length=10)
    store_id=models.CharField(max_length=7)
    source=models.CharField(choices=SOURCE_CHOICES, max_length=10)
    agent=models.ForeignKey("Agent", null = True, blank = True, on_delete=models.SET_NULL)
    category=models.ForeignKey("Category", related_name="complaints", null = True, blank = True, on_delete=models.SET_NULL)
    description = models.TextField()
    customer = models.ForeignKey("Customer", null = True, blank = True, on_delete=models.SET_NULL)

    def __str__(self):
        return f"{self.store_name} {self.store_id}"


class Category(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name



