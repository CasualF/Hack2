from django.db import models
from django.contrib.auth import get_user_model
from video.models import Video

User = get_user_model()


class Comment(models.Model):
    owner = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    attachment = models.FileField(upload_to=f'{video.title}/files', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner}|{self.video.title}|{self.content}'
