from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Teacher(models.Model):
    user = models.OneToOneField(User, related_name='teacher', on_delete=models.CASCADE)
    teacherName = models.CharField(max_length=200, verbose_name="teacherName")

    def __str__(self):
        return self.teacherName


class Student(models.Model):
    user = models.OneToOneField(User, related_name='student', on_delete=models.CASCADE)
    studentName = models.CharField(max_length=200, verbose_name="studentName")

    def __str__(self):
        return self.studentName


class Group(models.Model):
    student = models.ManyToManyField(Student, blank=True)
    teacher = models.ManyToManyField(Teacher, blank=True)
    groupName = models.CharField(max_length=200, verbose_name="groupName")

    def __str__(self):
        return self.groupName


class Exercise(models.Model):
    group = models.ForeignKey(Group, related_name='task', on_delete=models.CASCADE)
    teacher = models.ForeignKey(Teacher, related_name='task', on_delete=models.CASCADE)
    text = models.TextField(verbose_name="текст")

    def __str__(self):
        return self.text


class Solution(models.Model):
    exercise = models.ForeignKey(Exercise, related_name='decision', on_delete=models.CASCADE)
    student = models.ForeignKey(Student, related_name='decision', on_delete=models.CASCADE)
    text = models.TextField(verbose_name="текст")
    file = models.FileField(blank=True,  upload_to='uploads/')

    def __str__(self):
        return self.text

