from django.db import models
from django.contrib.auth import get_user_model
from video.models import Video

User = get_user_model()


class Comment(models.Model):
    owner = models.ForeignKey(User, related_name='comments', on_delete=models.CASCADE)
    video = models.ForeignKey(Video, related_name='comments', on_delete=models.CASCADE)
    content = models.TextField()
    attachment = models.FileField(upload_to=f'{video}/files', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.owner}|{self.video}|{self.content}'


class Rating(models.Model):
    RATING_CHOICES = (
        (1, 'Too bad'),
        (2, 'Bad'),
        (3, 'Normal'),
        (4, 'Good'),
        (5, 'Excellent')
    )
    video = models.ForeignKey(Video, related_name='ratings', on_delete=models.CASCADE)
    owner = models.ForeignKey(User, related_name='rating', on_delete=models.CASCADE)
    rating = models.PositiveSmallIntegerField(choices=RATING_CHOICES)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['owner', 'video']

    def __str__(self):
        return f'This video: {self.video} with rating: {self.rating}'


class Like(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='likes')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='likes')

    def __str__(self):
        return f'{self.owner.email} -> {self.video.title}'


class Favorite(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    video = models.ForeignKey(Video, on_delete=models.CASCADE, related_name='favorites')

    def __str__(self):
        return self.video.title
