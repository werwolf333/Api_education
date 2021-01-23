from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Client(models.Model):
    user = models.OneToOneField(User, related_name='client', on_delete=models.CASCADE)
    clientName = models.CharField(max_length=200, verbose_name="clientNameName")
    status = models.CharField(max_length=200, verbose_name="status")

    def __str__(self):
        return self.clientName


class Group(models.Model):
    client = models.ManyToManyField(Client, blank=True)
    groupName = models.CharField(max_length=200, verbose_name="groupName")

    def __str__(self):
        return self.groupName


class Exercise(models.Model):
    group = models.ForeignKey(Group, related_name='task', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Client, related_name='task', on_delete=models.CASCADE)
    text = models.TextField(verbose_name="текст")

    def __str__(self):
        return self.text


class Solution(models.Model):
    exercise = models.ForeignKey(Exercise, related_name='decision', on_delete=models.CASCADE)
    student = models.ForeignKey(Client, related_name='decision', on_delete=models.CASCADE)
    text = models.TextField(verbose_name="текст")
    file = models.FileField(blank=True,  upload_to='uploads/')

    def __str__(self):
        return self.text

