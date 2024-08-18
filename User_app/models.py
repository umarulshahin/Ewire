from django.db import models
from Authentication_app.models import *
from django.utils import timezone


class Post(models.Model):
    
    user = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    title = models.CharField(max_length=150,blank=False)
    description = models.TextField(blank=True)
    save_date = models.DateTimeField(default=timezone.now)
    publish = models.BooleanField(default=True,blank=False)
    
class User_Tag(models.Model):
    
    users = models.ForeignKey(CustomUser,on_delete=models.CASCADE,related_name='tagUser')
    post = models.ForeignKey(Post,on_delete=models.CASCADE,related_name='tagposts')
    
    class Meta:
        unique_together = ('post', 'users')

    def __str__(self):
        return f"{self.post.title} - {self.users.Username}"
    
    