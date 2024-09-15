from django.db import models

class Procedure(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    duration_minutes = models.PositiveIntegerField()

    def __str__(self):
        return self.name