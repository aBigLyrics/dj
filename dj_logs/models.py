
from django.contrib.auth.models import User
from django.db import models



# Create your models here.

class Topic(models.Model):
    """主题"""
    name = models.CharField(max_length=50)
    text = models.CharField(max_length=200)
    date_added = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Entry(models.Model):
    """学到的有关主题的具体知识"""

    topic = models.ForeignKey(Topic,on_delete=models.CASCADE)
    text = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural='entries'

    def __str__(self):

        return self.text[:50]+'...'
