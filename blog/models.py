from typing import Iterable
from django.db import models
import os
# Create your models here.
class Account(models.Model):
    class Role(models.TextChoices):
        ADMIN = 'ADMIN',
        USER = 'USER',
    created = models.DateTimeField(auto_now_add=True)
    username = models.CharField(max_length=100, blank=False)
    email = models.EmailField(max_length=100, blank=False)
    fullname = models.CharField(max_length=100, blank=False)
    password = models.CharField(max_length=100, blank=False)
    avatar = models.CharField(max_length=300, blank=True, default='')
    cover_image = models.CharField(max_length=300, blank=True, default='')
    role = models.CharField(
        max_length=5,
        choices=Role.choices,
        default=Role.USER,
    )
    
    class Meta:
        ordering = ['created']
    def save(self, *args, **kwargs):
        self.username = self.username.lower()
        self.email = self.email.lower()
        return super(Account, self).save(*args, **kwargs)
    

class Posts(models.Model):
    title = models.CharField(max_length=100, blank=False)
    content =  models.TextField(max_length=1000, blank=False)
    url = models.CharField(max_length=300, blank=True, default='')
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)


class Comments(models.Model):
    content =  models.TextField(max_length=1000, blank=False)
    url = models.CharField(max_length=300, blank=True, default='')
    account = models.ForeignKey(Account, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts,on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)