from django.db import models

# Create your models here.
class Tasklist(models.Model):
    task_name = models.CharField(max_length=250)
    task_description = models.TextField()
    start_date = models.DateField(auto_now=False, auto_now_add=False)
    end_date = models.DateField(auto_now=False, auto_now_add=False)
    assigned_by = models.IntegerField()
    assigned_to = models.IntegerField()
    status = models.IntegerField()

class Comment(models.Model):
    task_id = models.IntegerField()
    comment_by = models.IntegerField()
    description = models.TextField()
    date = models.DateTimeField(auto_now=False, auto_now_add=False)


