from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Url(models.Model):
    creator = models.ForeignKey(User,on_delete=models.CASCADE)
    link = models.CharField(max_length = 10000)
    uuid= models.CharField(max_length = 1000)
    created_on = models.DateTimeField(auto_now_add= True)

    def __str__(self):
        return self.link