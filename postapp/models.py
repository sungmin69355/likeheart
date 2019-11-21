from django.db import models
from django.contrib.auth.models import User

class Post(models.Model):
    title = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')
    body = models.TextField()
    name = models.CharField(max_length=50, null=True, blank=True)
    name_id = models.ForeignKey(User, on_delete = models.CASCADE, null=True)
    likes = models.ManyToManyField(User, related_name='likes')

    images = models.ImageField(blank=True, upload_to="usr", null=True)


    @property
    def total_likes(self):
        return self.likes.count()

    def __str__(self):
        return self.title

    def summary(self):
        return self.body[:100]
        
class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, related_name='comments')
    comment_date = models.DateTimeField('date published')
    comment_contents = models.CharField(max_length=200)
    comment_writer = models.CharField(max_length=50, null=True, blank=True)

    class Meta:
        ordering = ['-id']
            
    def __str__(self):
        return str(self.comment_writer)
