from django.db import models

# Create your models here.


class Task(models.Model):
    title = models.TextField()
    due_date = models.DateField()
    status = models.CharField(max_length = 10)
    parent = models.ForeignKey('Task', null=True, related_name='subtasks', on_delete=models.SET_NULL)
    deleted = models.BooleanField(default=False)
    deletion_date = models.DateField(null=True)
