from django.db import models
from django.contrib.auth.models import User
from datetime import datetime
from . import helper    

# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name


class Membership(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)


class Project(models.Model):
    name = models.CharField(max_length=30)
    description = models.TextField()
    endDate = models.DateField()
    avatar = models.ImageField(
                upload_to=helper.path_and_rename,
                default='avatar/default.png'
                )
    team = models.ForeignKey(Team, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Task(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=30)
    description = models.TextField()
    startDate = models.DateField()
    endDate = models.DateField()

    def __str__(self):
        return self.name

class ToDo(models.Model):
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    todo = models.TextField()
    status = models.BooleanField()

    def __str__(self):
        return self.todo