from django.db import models
from django.contrib.auth.models import User


class Tab(models.Model):
    DIFFICULTY_CHOICES = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
    ]

    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='tabs')
    title = models.CharField(max_length=200)
    artist = models.CharField(max_length=200)
    song = models.CharField(max_length=200)
    tuning = models.CharField(max_length=50, default='Standard (EADGBe)')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_CHOICES, default='beginner')
    content = models.TextField()
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} — {self.artist}"


class Comment(models.Model):
    tab = models.ForeignKey(Tab, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author.username} on {self.tab.title}"


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    tab = models.ForeignKey(Tab, on_delete=models.CASCADE, related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'tab')

    def __str__(self):
        return f"{self.user.username} ♥ {self.tab.title}"