from django.contrib.auth import get_user_model
from django.db import models



# Create your models here.

User = get_user_model()
class Video(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    video_url = models.FileField(upload_to=True)
    time = models.DateTimeField()
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account')


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'video'
        verbose_name_plural = 'videos'