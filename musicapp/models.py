from distutils.command.upload import upload
from django.contrib.auth.models import User
from django.db import models

# Create your models here.

class Song(models.Model):
    Language_Choice = (
        ('Hindi', 'Hindi'),
        ('English', 'English'),
    )
    Mood_Choice = (
        ('Happy', 'Happy'),
        ('Sad', 'Sad'),
        ('Fear', 'Fear'),
        ('Angry', 'Angry'),
        ('Neutral', 'Neutral'),
        ('Non', 'Non'),
    )
    song_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=2000)
    artist = models.CharField(max_length=2000)
    mood = models.CharField(max_length=20, choices=Mood_Choice, default='Non')
    language = models.CharField(max_length=20, choices=Language_Choice, default='Hindi')
    tags = models.CharField(max_length=100)
    image = models.ImageField()
    song_file = models.FileField()

    def __str__(self):
        return self.name


class Playlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    playlist_name = models.CharField(max_length=200)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)



class Favourite(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    is_fav = models.BooleanField(default=False)


class Recent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)

