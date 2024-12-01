from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import datetime

def figureout(note):
    if "C#" in note or "Db" in note:
        return "C#(Db)"
    elif "D#" in note or "Eb" in note:
        return "D#(Eb)"
    elif "F#" in note or "Gb" in note:
        return "F#(Gb)"
    elif "G#" in note or "Ab" in note:
        return "G#(Ab)"
    elif "A#" in note or "Bb" in note:
        return "A#(Bb)"
    else:
        return note

# Create your models here.
class Scale(models.Model):
    scale_name = models.TextField(blank=False)
    I = models.TextField(blank=False)
    II = models.TextField(blank=False)
    III = models.TextField(blank=False)
    IV = models.TextField(blank=False)
    V = models.TextField(blank=False)
    VI = models.TextField(blank=False)
    VII = models.TextField(blank=False)

    def __str__(self):
        return f'{self.scale_name} {self.I} {self.II} {self.III} {self.IV} {self.V} {self.VI} {self.VII}'
    
def scale_load_data():
    filename = 'C:/Users/scales.csv'
    f = open(filename)
    f.readline()
    for line in f:
        fields = line.split(', ')
        try:
            scale = Scale(scale_name = fields[0], 
                          I = figureout(fields[1]), 
                          II=figureout(fields[2]), 
                          III=figureout(fields[3]), 
                          IV=figureout(fields[4]), 
                          V=figureout(fields[5]), 
                          VI=figureout(fields[6]), 
                          VII=figureout(fields[7].replace("\n", ""))
                          )
            scale.save()
        except:
            print(f"Skipped: {fields}")
    
    print(f'Done. Created {len(Scale.objects.all())} Results.')


# IMPORTANT models

class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    chords_foreignkeys = models.JSONField()
    image_file = models.ImageField(blank=True)
    display_name = models.TextField(blank=True)
    def __str__(self):
        hi = self.chords_foreignkeys["list"]
        return f'{self.user} | Learned Chords: {hi}'

class Chord(models.Model):
    chord_name = models.TextField(blank=False)
    notes = models.JSONField()
    image_url = models.URLField(blank=True)
    audio_url = models.URLField(blank=True)
    def __str__(self):
        hi = self.notes['list']
        return f'{self.chord_name} {hi}'

class Artist(models.Model):
    name = models.TextField(blank=False)
    image_url = models.URLField(blank=True)
    def __str__(self):
        return f'{self.name}'

class Song(models.Model):
    chords_foreignkeys = models.JSONField() # Note: foreign key is a misnomer! should be a list strings!
    lyrics = models.TextField(blank=False) 
    score_link = models.URLField(blank=True)
    # added_by_user = models.ForeignKey(User, on_delete=models.CASCADE)
    artist = models.ForeignKey("Artist", on_delete = models.CASCADE)
    song_name = models.TextField(blank=True)
    users_and_their_progresses = models.JSONField()
    capo_info = models.IntegerField(blank=True)
    additional_info = models.TextField(blank=True)

    spotify_link = models.URLField(blank=True)
    vimeo_link = models.URLField(blank=True)

    def __str__(self):
        hi = self.chords_foreignkeys['list']
        return f'{self.song_name} by {self.artist}, chords: {hi}'


class Recording(models.Model):
    audio = models.FileField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.datetime.now)
