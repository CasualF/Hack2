from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Video(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    file = models.FileField(upload_to=True)
    created_at = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='account')

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'video'
        verbose_name_plural = 'videos'
