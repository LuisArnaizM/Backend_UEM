from django.db import models

class User(models.Model):
    username = models.CharField(max_length=100)
    email = models.EmailField()
    date_joined = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.username


class Preference(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    favorite_artist = models.CharField(max_length=100)
    favorite_song = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.user.username}'s preference"
