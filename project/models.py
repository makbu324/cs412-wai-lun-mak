from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField
import datetime

# The function determines the flat/sharp notes and sees which one is equivalent to what note.
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

# This model is currently unused. 
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

# The load data function was intially used to load chords into the database.
# I later found out that chords can be webscraped.
# Therefore the function below did not pose any use.
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


### ### IMPORTANT MODELS ### ###

# The user stores: 
# 1. what chords the user knows, 
# 2. the associated user, the user profile pic, 
# 3. and the display name of the user account.
class UserInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE) 
    chords_foreignkeys = models.JSONField()
    image_file = models.ImageField(blank=True)
    display_name = models.TextField(blank=True)
    def __str__(self):
        hi = self.chords_foreignkeys["list"]
        return f'{self.user} | Learned Chords: {hi}'

# There are at max 6 notes on a guitar chord.
# There is a webscraped image/audio file attached to a Chord model.
# The chord name helps identify what chord we are talking about.
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

# A Song Model stores:
# 1. what chords are used on it, 
# 2. the lyrics and chords side by side 
# 3. the Ultimate Guitar Tab score link this is scrapped from
# 4. the artist who made this song 
# 5. the song name 
# 6. which user has finished learning the song, which user hasnt finished learning this song
# 7. the capo the song requires
# 8. the additional info: tuning 
# 9. the attached spotify song
# 10. the webscraped music video link (if there is one) (provided by vimeo)
class Song(models.Model):
    chords_foreignkeys = models.JSONField() # Note: "foreign key" is a misnomer! Should be called a list of strings!
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

# A Recording Model stores:
# 1. audio file itself
# 2. the user who recorded it
# 3. the song that this recording is doing a cover of
# 4. date that this recording was made
class Recording(models.Model):
    audio = models.FileField(blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    date = models.DateTimeField(default=datetime.datetime.now)
