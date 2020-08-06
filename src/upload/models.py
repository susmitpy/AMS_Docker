from django.db import models

# Create your models here.
class Division(models.Model):
    name = models.CharField(max_length = 5, default="")

    def __str__(self):
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=20,default="")
    code = models.CharField(max_length=5,default="")

    def __str__(self):
        return self.name
