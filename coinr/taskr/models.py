import logging
from django.db import models
from django.contrib.postgres.fields import ArrayField

# Create your models here.
class CoinTask(models.Model):
    """
    Stores coin tasks with enriched data
    """
    id = models.CharField(primary_key=True, max_length=20)
    exchanges = ArrayField(models.CharField(max_length=20), default=list, size=1000)
    task_run = models.IntegerField(null=False, blank=False)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)

    def coin_id_exists(self, id: str) -> bool:
        return CoinTask.objects.filter(id=id).exists()

class TaskCount(models.Model):
    """
    Keeps track of number of tasks sent
    """
    id = models.CharField(primary_key=True, max_length=20)
    counter = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True, null=True)
    updated_at = models.DateTimeField(auto_now=True, null=True)


