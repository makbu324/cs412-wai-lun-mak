from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views.generic import ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import * 
import plotly
import plotly.graph_objs as go
from django.shortcuts import render
import requests
from .forms import *

# This view allows the user to create a new account: username and password
# This view will automatically create a UserInfo object
class RegistrationView(CreateView):
    template_name = 'project/register.html'
    form_class = UserCreationForm

    # this dispatch method will create the UserInfo model object, only if the form is correct!
    def dispatch(self, *args, **kwargs):
        if self.request.POST:
            user_form = UserCreationForm(self.request.POST)
            if not user_form.is_valid():
                print("error!")
                return super().dispatch(*args, **kwargs)
            user = user_form.save()    

            # logins the user in 
            login(self.request, user)
            UserInfo.objects.create(user=user, chords_foreignkeys={'list': []})
            
            return redirect(reverse('search_songs'))
        
        return super().dispatch(*args, **kwargs)

# The webscraping function for looking up songs on Ultimate Guitar Tabs
def get_content(product):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.ultimate-guitar.com/search.php?search_type=title&value={product}').text
    return html_content

# The webscraping function for looking up spotify songs, vimeo videos, information for chords, e.t.c.
def get_html(url):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(url).text
    return html_content

# the notes on a piano
scale = ["C", "C#(Db)", "D", "D#(Eb)", "E", "F" ,"F#(Gb)", "G" ,"G#(Ab)", "A" ,"A#(Bb)", "B"]

# This function helps resolve notes that are flat or sharp (make them the same thing)
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
    
# Allows the guitar notes to be translated onto piano notes
tuning = ["E", "A", "D", "G", "B", "E"]

# Helps figure out the correct note on the guitar fretboard
def semitone(note, level):
    ii = scale.index(note)
    while level > 0:
        level -= 1
        if ii == len(scale)-1:
            ii = 0
        else:
            ii += 1
    return scale[ii]

# This function helps to fetch the notes on the guitar fretboard (by reading the string of the url link of the image of the guitar fingering.)
def find_notes_string(s):
    s = s.replace("/images/chordshape/", "").replace(".png", "")
    while "-" in s:
        s = s[s.index("-")+1:]
    on = True
    list = []
    build = ""
    note_index = 0
    for ch in s:
        if ch == "%":
            on = False
            try:
                list += [semitone(tuning[note_index], int(build))]
            except:
                ""
            note_index += 1
        elif on == False and not ch in "1234567890x":
            on = True
            build = ""
        if on and ch in "1234567890x":
            build += ch
    try:
        list += [semitone(tuning[note_index], int(build))]
    except:
        ""
    return list

# There is usually a number attached a tab link provided by Ultimate Guitar Tab. 
# This function is built so that we can give a "serial number" for each song tab
def getVersionNumber(s):
    the_string = ""
    for c in reversed(s):
        if c in "1234567890":
            the_string = c + the_string
        else:
            break
    return the_string

### *** The View Class for the user to look up songs by webscraping. ***  ###
def search_songs(request):
    # The webscraped content
    html_content = ""

    # The webscraped tab content
    contents_baby = ""

    # The chords of the song
    CHORDS = []

    # The song's artist
    artist_name = ""

    # The song name
    song_name = ""

    # The tuning/capo of the song tab
    song_info = ""

    # The capo of the song tab
    capo_info = ""

    # The chord's notes, audio file, and image file (all webscraped from the internet!)
    chords_info = []

    # The artist's profile pic
    the_artist_image = ""

    # The other song tab links that the user can try 
    url_stuff = []

    # The Ultimate Guitar Tab link of this song's tab (the tab in display)
    url_link = ""

    # The music video related to this song
    yt_url = ""

    # The spotify song related to this song
    spotify_url = ""

    # The "serial number" of this tab
    ver = ""

    # Has the user learned this song yet?
    stat= ""

    # Did the user tell the webscraper to look for its search query?
    if 'product' in request.GET or 'learn_song' in request.GET :
        # urls
        product = request.GET.get('product')
        html_content = get_content(product)
        
        # The part that the webscraper has to look for (for the artist profile pic)
        key_thing = "https://www.ultimate-guitar.com/static/s3/ugdb/media/cover/artist/"
        see = html_content.count(key_thing)

        # The part that the webscraper has to look for (for the tab link)
        tab_thing = "https://tabs.ultimate-guitar.com/tab/"

        for time in range(see):
            image_first = html_content.index(key_thing)
            html_content = html_content[image_first:]
            image_last = html_content.index("@300")
            profile_pic = html_content[:image_last]

            tab_first = html_content.index(tab_thing)
            test = html_content[tab_first:]
            tab_last = test.index("&quot;")
            tab_url = test[:tab_last]

            try:
                sn_first = html_content.index("song_name")
                test = html_content[sn_first:]
                song_name_is = test[:test.index("artist_id")]
                song_name_is = song_name_is.replace("song_name", "").replace("&quot", "").replace(";","").replace(",","").replace(":","")

                an_first = html_content.index("artist_name")
                artist_name_is = html_content[an_first:html_content.index("type")]
                artist_name_is = artist_name_is.replace("artist_name", "").replace("&quot", "").replace(";","").replace(",","").replace(":","")

                # If the song name is too long, something is out of place. Skip it.
                if (len(song_name_is) > 70 or len(artist_name_is) >  70):
                    break
                
                # print(profile_pic)
                # print(tab_url)
                # print(song_name_is)
                # print(artist_name_is)

                version = ""
                for c in reversed(tab_url):
                    if c in "1234567890":
                        version = c + version
                    else:
                        break

                # for displaying song links in the "Similar Songs" section
                url_stuff += [[profile_pic,tab_url,song_name_is,artist_name_is, version]]
            except:
                #print("DONE")
                break
            html_content = html_content[image_last+5:]
            
        # If the user previously requested for a song tab, we should display that song tab on screen.
        if 'learn_song_link' in request.GET:
            the_artist_image = request.GET['image_link']
            the_tab_url = request.GET['learn_song_link']
            url_link = the_tab_url
            ver = getVersionNumber(the_tab_url)
        elif len(url_stuff) > 0:
            the_artist_image = url_stuff[0][0]
            the_tab_url = url_stuff[0][1]
            url_link = the_tab_url
            ver = getVersionNumber(the_tab_url)

        # THE CONTENTS OF THE WEBSCRAPED SONG
        song_content = ""
        try:
            song_content=""
            song_content = get_html(the_tab_url)
            ii = song_content.index("\"text\": \"")
            song_info = song_content[ii+9: ii+100]
            song_info = song_info[: song_info.index('"')].replace(" Tuning", " \nTuning").replace(" Key", " \nKey").replace(" Capo", " \nCapo")
            capo_info = song_info[song_info.index("Capo:"):]
            song_info = song_info.replace(capo_info, "")
        except:
            ""
        user_id_found = False

        # We start to look for the information related for the webscraped song below.
        for index, character in enumerate(song_content):
            if artist_name == "":
                if song_content[index: index+11] == "artist_name":
                    a_n = song_content[index+24 : index+124]
                    artist_name = a_n[: a_n.index('&quot')].replace("&amp;", "&")
            if song_name == "":
                if song_content[index: index+9] == "song_name":
                    s_n = song_content[index+22 : index+124]
                    song_name = s_n[: s_n.index('&quot')]
            if song_content[index: index+8] == "wiki_tab":
                user_id_found = True
            if user_id_found:
                contents_baby += character
                if character == ']':
                    if song_content[index+1] in "ABCDEFG":
                        the_chord = song_content[index+1: index+20]
                        try:
                            the_chord = the_chord[: the_chord.index('[')]
                            if not the_chord in CHORDS:
                                CHORDS += [the_chord]
                        except:
                            ""

                # We see if the webscraped content has any problem. If there is, just let the user know that they should try another song.
                if song_content[index: index+11] == "revision_id":
                    contents_baby = contents_baby.replace("&quot", "").replace(r'\n', '"\n"').replace(r'\r', '').replace('[tab]', '').replace('[/tab]', '').replace('"', '').replace('&#039;', "'").replace('[ch]', '').replace('[/ch]', '').replace('&rsquo;', "'")[0:] 
                    try:
                        contents_baby = contents_baby[contents_baby.index("content;:;")+10:-4]
                    except:
                        contents_baby = "Unfortunately, this song cannot be accessed currently! Please try another song!"
                        stat = "nope"
                    break

        ## See if song is already added in the database
        this_song_exists = Song.objects.filter(score_link=url_link)

        # Time to look for the information related to the chords used in the song. 
        for chord in CHORDS:
            lookup = chord.replace("#", "%23")

            # I used JGuitar to extract the audio file and chord files 
            chord_content = get_html(f'https://jguitar.com/chordsearch?chordsearch={lookup}')
            image_c = ""
            try:
                # the image displaying the fingering position of the chord
                ic = chord_content.index("\"/images/chordshape/")
                image_c = chord_content[ic: ic+100]
                image_c = image_c[2:image_c.index("\" alt=")]
            except:
                ""

            audio_c = ""
            try:
                # the audio file of the chord
                ac = chord_content.index("\"/audio/chordshape/")
                audio_c = chord_content[ac: ac+100]
                audio_c = audio_c[2:audio_c.index("\" title=")]
            except:
                ""
            
            if not image_c == "" and not audio_c == "" and ".png" in image_c and (not "{" in image_c or not "(" in image_c):
                chords_info += [["https://jguitar.com/" + image_c, "https://jguitar.com/" + audio_c, find_notes_string(image_c), lookup.replace("%23", "#")]]

        # This section looks for the vimeo link related to the song
        try:
            keyword = song_name + " " + artist_name + " vimeo"
            search = "https://www.google.com/search?q=" + keyword.replace(" ", "+")
            yt_content = get_html(search)
            yt_scrape = yt_content[yt_content.index("https://vimeo.com/")+len("https://vimeo.com/"):]
            times = 0 
            while "channels" in yt_scrape[:100] or "groups" in yt_scrape[:100] or "ondemand" in yt_scrape[:100]:
                print(yt_scrape[:100] )
                times += 1
                if (times > 2):
                    break 
                yt_scrape = yt_scrape[100:]
                yt_scrape = yt_content[yt_content.index("https://vimeo.com/")+len("https://vimeo.com/"):]
            yt_scrape = yt_scrape[:yt_scrape.index('&amp')]
            yt_url = f"https://player.vimeo.com/video/{yt_scrape}?badge=0&amp;autopause=0"
            print("HERE: " + yt_url)
        except:
            "" 

        if yt_url == "": # This section tries again if a music video has not been found.
            try:
                keyword = song_name + " " + artist_name + " vimeo"
                search = "https://www.google.com/search?q=" + keyword.replace(" ", "+")
                yt_content = get_html(search)
                yt_scrape = yt_content[yt_content.index("videos/")+len("videos/"):]
                times = 0 
                while "channels" in yt_scrape[:100] or "groups" in yt_scrape[:100] or "ondemand" in yt_scrape[:100]:
                    print(yt_scrape[:100] )
                    times += 1
                    if (times > 2):
                        break 
                    yt_scrape = yt_scrape[100:]
                    yt_scrape = yt_content[yt_content.index("videos/")+len("videos/"):]
                yt_scrape = yt_scrape[:yt_scrape.index('&amp')]
                yt_url = f"https://player.vimeo.com/video/{yt_scrape}?badge=0&amp;autopause=0"
                print("HERE: " + yt_url)
            except:
                "" 

        # This section searches for the related spotify song of this tab.
        try:
            keyword = song_name + " " + artist_name + " spotify "
            search = "https://www.google.com/search?q=" + keyword.replace(" ", "+") + "&ia=web"
            yt_content = get_html(search)
            yt_scrape = yt_content[yt_content.index("https://open.spotify.com/track/")+len("https://open.spotify.com/track/"):]
            yt_scrape = yt_scrape[:yt_scrape.index('&amp;')]
            spotify_url = "https://open.spotify.com/embed/track/"+ yt_scrape + "?utm_source=generator"
            print("HERE: " + spotify_url)
        except:
            ""

        # filter only the tab that is being displayed
        filter_other_songs = []
        for l in url_stuff:
            if not l[1] == url_link:
                filter_other_songs += [l]
        url_stuff = filter_other_songs

        # Sees if the user has requested to add this song into their "songs-in-progress" list.
        if  "add_song" in request.POST and not(song_name == "") and len(contents_baby) > 100:
            artistName = artist_name
            artist_list = Artist.objects.filter(name=artistName)
            capo = -1
            if not capo_info == "":
                cp = capo_info.split(" ")
                if cp[1][0] in "1234567890":
                    capo = int(cp[1])

            if list(artist_list) == []:
                Artist.objects.create(name=artistName, image_url=the_artist_image)
                artist_list = Artist.objects.filter(name=artistName)
            
            song_list = Song.objects.filter(score_link = url_link)

            # If the user previously requested, we should respect it.
            ## note: if the song was added previously in the databse, we just modify the JsonList of the song.
            if request.POST["add_link"] == "no":
                print("don't add video!")
                yt_url = ""

            if list(song_list) == []:
                # This means that the song is new and needs to be added to the database.
                hi = Song.objects.create(chords_foreignkeys = {"list": CHORDS}, 
                                        lyrics=contents_baby, 
                                        score_link = url_link, 
                                        artist = artist_list[0], 
                                        song_name = song_name, 
                                        users_and_their_progresses = {"list": [ [request.user.pk, False] ]}, 
                                        capo_info = capo, additional_info = song_info, 
                                        spotify_link=spotify_url, 
                                        vimeo_link = yt_url)
            
                print("Song " + str(hi) + " created")
            elif not list(this_song_exists) == []:
                # This section happens if the song turns to be already added in the database.
                the_song = list(this_song_exists)[0]
                users_from_song = the_song.users_and_their_progresses["list"]
                users_from_song += [[request.user.pk, False]]
                Song.objects.filter(score_link=url_link).update(users_and_their_progresses = {"list": users_from_song})

            # Add new chords that are not in the database!
            for l in chords_info:
                image_link = l[0]
                audio_link = l[1]
                the_notes = l[2]
                chord_name = l[3]
                chord_list = Chord.objects.filter(chord_name=chord_name)
                if list(chord_list) == []:
                    ch = Chord.objects.create(chord_name=chord_name,
                                              notes={"list": the_notes},
                                              image_url=image_link,
                                              audio_url=audio_link)


        ## tests if the song is already added or not (for debugging)
        ## It also checks if the user already owns the song
        if not list(this_song_exists) == []:
            users_from_song = list(this_song_exists)[0].users_and_their_progresses["list"]
            for l in users_from_song:
                if l[0] == request.user.pk:
                    stat = "already added"
                    print("ALREADY ADDED")
                    break
    
    print("vimeo link? ", yt_url)

    return render( request, "project/search_songs.html", {'lyrics': contents_baby, "artist_name" : artist_name, "chords": CHORDS, "song_name": song_name, "chords_info": chords_info, "song_info": song_info, "the_artist_image": the_artist_image, "url_stuff": url_stuff, "url_link": url_link, "spotify_url": spotify_url, "item": yt_url, "capo_stuff": capo_info, "ver": ver, "status": stat})

## END OF "SEARCH SONGS" VIEW ##


# Show all artists already added in the database (can always be expanded!)
class ShowAllArtists(ListView):
    model = Artist
    template_name = "project/show_all_artists.html"
    context_object_name = "artists"

# Show all chords already added in the database (can always be expanded!)
class ShowAllChords(ListView):
    model = Chord
    template_name = "project/show_all_chords.html"
    context_object_name = "chords"

# Show all songs already added in the database (can always be expanded!)
# The song will be displayed as orange if the user hasn't finished learning the song, 
# or green if they finished learning, or blue if they haven't added the song.
class ShowAllSongs(ListView):
    model = Song
    template_name = "project/show_all_songs.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        songs = []
        for song in Song.objects.all().order_by('song_name'):
            already_learned = ""
            if self.request.user.is_authenticated:
                for l in song.users_and_their_progresses["list"]:
                    if l[0] == self.request.user.pk:
                        if not l[1]:
                            already_learned = "in progress" # the user is not done with learning the song
                        elif l[1]:
                            already_learned = "yes" # the user is done with learning the song
            songs += [[song, getVersionNumber(song.score_link), already_learned]]
        context["songs"] = songs
        return context

## The page displays the summarized information of other users on the web application.
class ShowAllUsers(ListView):
    model = UserInfo
    template_name = "project/show_all_users.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = []
        for ui in UserInfo.objects.all():
            songs_learned = 0 # how many songs this user has learned.
            songs_learning = 0 # how many songs this user is not done learning.
            chords_learned = len(ui.chords_foreignkeys["list"]) # how many chords this user "owns" :)
            recordings = 0 # how many recordings did they put out on this web app
            for song in Song.objects.all():
                for l in song.users_and_their_progresses["list"]:
                    if l[0] == ui.user.pk:
                        if l[1] == True:
                            songs_learned += 1
                        else:
                            songs_learning += 1
            for au in Recording.objects.all():
                if au.user == ui.user:
                    recordings += 1
            
            current_user = False

            # Sees if the user is the current viewing user
            # If yes, display the border of their avatar image in green!
            if ui.user == self.request.user:
                current_user = True
            
            users += [[ui, songs_learned,songs_learning,chords_learned,recordings,current_user]]

        context["users"] = users
        return context

# This view displays a song added in the database. 
class ShowSong(DetailView):
    model = Song
    template_name = "project/song.html"
    context_object_name = "s"

    def post(self, request, *args, **kwargs):
        # The user deletes the posted audio (that belongs to them, can't be deleting others'...)
        if "delete_audio" in request.POST:
            pk_to_delete = int(request.POST["delete_audio"])
            Recording.objects.filter(pk=pk_to_delete).delete()

        # This indicates that the user has already learned this song
        if "learned_this_song" in request.POST:
            the_song = Song.objects.get(pk=self.kwargs['pk'])
            users_from_song = the_song.users_and_their_progresses["list"]
            for i, l in enumerate(users_from_song):
                if l[0] == self.request.user.pk:
                    users_from_song[i][1] = True
            Song.objects.filter(pk=self.kwargs['pk']).update(users_and_their_progresses={"list": users_from_song})

        # This indicates that the user recently sent a request to add this song into their "songs-in-progress" list
        if "add_this_song_to_learn" in request.POST:
            the_song = Song.objects.get(pk=self.kwargs['pk'])
            users_from_song = the_song.users_and_their_progresses["list"]
            users_from_song += [[self.request.user.pk, False]]
            Song.objects.filter(pk=self.kwargs['pk']).update(users_and_their_progresses= {"list": users_from_song})
            
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        # This is a signal that the recorded audio should be added to the database
        if is_ajax:
            audio_file = request.FILES.get('recorded_audio')
            print("RECORDING DONE.")
            song = Song.objects.get(pk=self.kwargs['pk'])
            Recording.objects.create(audio = audio_file, user= request.user,song=song)

        return redirect(reverse('song', kwargs = {'pk':self.kwargs['pk']})) 

    # The displaying html needs context!
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        song = Song.objects.get(pk=self.kwargs['pk'])
        songName = song.song_name
        users_and_prog = song.users_and_their_progresses["list"]
        
        ## chs = the name of the chords that are used in the song
        chs = song.chords_foreignkeys["list"]
        context["artist"] = song.artist
        context["chords"] = chs
        context["item"] = song.vimeo_link 

        chord_things = []

        learned_chords = []
        if self.request.user.is_authenticated:
            learned_chords = UserInfo.objects.get(user=self.request.user).chords_foreignkeys["list"]

        # All the songs used in this song
        for ch in Chord.objects.all():
            if ch.chord_name in chs:
                learned = False
                if ch.chord_name in learned_chords:
                    learned = True
                chord_things += [[ch.image_url, ch.audio_url, ch.notes["list"], ch.pk, learned]]

        context["chords_info"] = chord_things

        ## access audio
        recordings = []
        for r in Recording.objects.all():
            is_user = False
            if self.request.user == r.user:
                is_user = True
            if r.song.song_name == songName:
                recordings += [[r, UserInfo.objects.get(user=r.user), is_user]]

        context["recordings"] = recordings

        ## has the user not added the song?
        not_added = False
        if self.request.user.is_authenticated:
            not_added = True
            for up in users_and_prog:
                if up[0] == self.request.user.pk:
                    not_added = False
                    break

        context["not_added"] = not_added

        ## has the user learned all chords?
        learned_all = False
        if self.request.user.is_authenticated:
            learned_all = True
            for chord in chs:
                if not chord in learned_chords:
                    learned_all = False
                    break

        context["learned_all"] = learned_all

        already_learned = False

        # Sees if the user has already learned the song or not
        if self.request.user.is_authenticated:
            song = Song.objects.get(pk=self.kwargs['pk'])
            u_a_p = song.users_and_their_progresses["list"]
            for i in range(len(u_a_p)):
                l = u_a_p[i]
                if l[0] == self.request.user.pk and l[1]:
                    already_learned = True
                    break


        context["already_learned"] = already_learned

        return context

# All the notes on the displaying piano in the "individual chord" page  
keyboard = ["E", "F" ,"F#(Gb)", "G" ,"G#(Ab)", "A" ,"A#(Bb)", "B", "C", "C#(Db)", "D", "D#(Eb)", "E", "F" ,"F#(Gb)", "G" ,"G#(Ab)", "A" ,"A#(Bb)", "B","C", "C#(Db)", "D", "D#(Eb)", "E", "F" ,"F#(Gb)", "G" ,"G#(Ab)", "A" ,"A#(Bb)", "B", "C", "C#(Db)", "D", "D#(Eb)", "E", "F" ,"F#(Gb)", "G" ,"G#(Ab)", "A" ,"A#(Bb)", "B"]

# All the audio files stored in the static folder (for playing piano sound)
n_files = ["-e", "-f" ,"-fs", "-g" ,"-gs", "-a" ,"-as", "-b", "-c", "-cs", "-d", "-ds", "-e", "-f" ,"-fs", "-g" ,"-gs", "-a" ,"-as", "-b","-c", "-cs", "-d", "-ds", "-e", "-f" ,"-fs", "-g" ,"-gs", "-a" ,"-as", "-b", "-c", "-cs", "-d", "-ds", "-e", "-f" ,"-fs", "-g" ,"-gs", "-a" ,"-as", "-b"]

# The "individual chord" page
class ShowChord(DetailView):
    model = Chord
    template_name = "project/chord.html"
    context_object_name = "c"

    def post(self, request, *args, **kwargs):
        chord = Chord.objects.get(pk=self.kwargs['pk'])
        chordName = chord.chord_name

        # The user told the web app that they have already learned this song
        if "learned" in request.POST:
            userInfo = UserInfo.objects.get(user=self.request.user)
            learned_chords = userInfo.chords_foreignkeys["list"]
            learned_chords += [chordName]
            UserInfo.objects.filter(user=self.request.user).update(chords_foreignkeys = {"list": learned_chords})

        return redirect(reverse('chord', kwargs = {'pk':self.kwargs['pk']})) 
        
    # The displaying html needs context!
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chord = Chord.objects.get(pk=self.kwargs['pk'])
        
        # The link redirects the user to the page displaying other variations of this chord (Provided by JGuitar)
        context["lookup_more"] = "https://jguitar.com/chordsearch?chordsearch=" + chord.chord_name
        chordNotes = chord.notes["list"]
        context["chords"] = chordNotes
        instructions = []
        media_notes = []
        ii = 0
        level = 2
        j = -1

        # This for-loop translates the guitar chord into a piano chord
        for k in keyboard:
            j += 1
            if k == "C":
                level += 1
            if ii == len(chordNotes):
                if "(" in k:
                    instructions += [["black-key", "playNote(\"" + str(level) + n_files[j] + "\")"]]
                else:
                    instructions += [["white-key", "playNote(\"" + str(level) + n_files[j] + "\")"]]
            elif k == chordNotes[ii]:
                if "(" in k:
                    instructions += [["black-red-key", "playNote(\"" + str(level) + n_files[j] + "\")"]]
                else:
                    instructions += [["white-red-key", "playNote(\"" + str(level) + n_files[j] + "\")"]]
                ii += 1
            else:
                if "(" in k:
                    instructions += [["black-key", "playNote(\"" + str(level) + n_files[j] + "\")"]]
                else:
                    instructions += [["white-key", "playNote(\"" + str(level) + n_files[j] + "\")"]]
            media_notes += [[str(level) + n_files[j], "/static/" + str(level) + n_files[j] + ".wav"]]

        context["night_and_day"] = instructions
        context["media_notes"] = media_notes

        ## Songs that use this chord
        chordName = chord.chord_name
        related_songs = []
        for song in Song.objects.all():
            chordsList = song.chords_foreignkeys["list"]
            if chordName in chordsList:
                related_songs += [[song.song_name, song.artist.name, getVersionNumber(song.score_link), song.artist.image_url, song.pk]]
                print(song.pk)
        context["related_songs"] = related_songs

        ## Whether the user has learned the displaying chord or not
        learn = ""
        if self.request.user.is_authenticated:
            userInfo = UserInfo.objects.get(user=self.request.user)
            if chordName in userInfo.chords_foreignkeys["list"]:
                learn = "user_learned"
            else:
                learn = "user_hasnt"
        
        context["learn"] = learn

        return context
    

# This view used for the user to update their profile pic/display name
class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model= UserInfo
    form_class = UpdateUserInfoForm
    context_object_name = "ui"
    template_name = "project/update_userinfo_form.html"

    def get_object(self):
        return UserInfo.objects.get(user=self.request.user)

    def dispatch(self, request, *args, **kwargs):
        userinfo = UserInfo.objects.get(user=self.request.user)

        if request.user == userinfo.user:
            return super().dispatch(request, *args, **kwargs)
        else:
            return redirect(reverse('show_all_users')) 
        
    def get_success_url(self):
        return reverse("show_all_users")

# This page shows how frequent a chord is used by the specific artist, and what songs the artist has written (present in the database).   
class ShowArtist(DetailView):
    model = Artist
    template_name = "project/show_artist.html"
    context_object_name = "a"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        artist = Artist.objects.get(pk=self.kwargs['pk'])
        artistName = artist.name
        songs = []
        x = []
        y = []

        # Creating the ListView of songs writtened by the artist
        for song in Song.objects.all():
            if song.artist.name == artistName:
                songs += [[song, getVersionNumber(song.score_link)]]
                for chord in song.chords_foreignkeys["list"]:
                    if not chord in x:
                        x += [chord]
                        y += [1]
                    else:
                        ii = x.index(chord)
                        y[ii] += 1

        # This creates the graph that shows the frequency of chords used by the artist on display
        fig = go.Bar(x=x, y=y)
        bar_div = plotly.offline.plot({'data': [fig]},
                                      auto_open=False,
                                      output_type='div',)
        
        context['bar_div'] = bar_div
        context["songs"] = songs
        context["song_count"] = len(songs)


        return context






## Displays the information of an individual user on the web app
class ShowUserInfo(DetailView):
    model = UserInfo
    template_name = "project/show_userinfo.html"
    context_object_name = "ui"
    def post(self, request, *args, **kwargs):
        # Detects if the user requested to delete one of their audio recordings
        if "delete_audio" in request.POST:
            pk_to_delete = int(request.POST["delete_audio"])
            Recording.objects.filter(pk=pk_to_delete).delete()

        return redirect(reverse('user_info', kwargs = {'pk':self.kwargs['pk']}))
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userInfo = UserInfo.objects.get(pk=self.kwargs['pk'])

        ## Songs in progress and learned
        songs_in_progress = []
        songs_learned = []
        for song in Song.objects.all():
            for l in song.users_and_their_progresses["list"]:
                if l[0] == userInfo.user.pk:
                    if not l[1]:
                        songs_in_progress += [[song, getVersionNumber(song.score_link)]]
                    elif l[1]:
                        songs_learned += [[song, getVersionNumber(song.score_link)]]
        context["songs_in_progress"] = songs_in_progress
        context["songs_learned"] = songs_learned

        display_name = "User: " + userInfo.user.username
        if not userInfo.display_name == "":
            display_name = userInfo.display_name
        context["display_name"] = display_name

        ## Is it the current viewing user?  
        ## If yes, give them permisison to modify their "UserInfo" model
        current_user = False
        if self.request.user == userInfo.user:
            current_user = True
        context["current_user"] = current_user
        
        ## The "chord vault" of the user
        chord_things = []

        for ch in userInfo.chords_foreignkeys["list"]:
            chord = Chord.objects.get(chord_name=ch)
            chord_things += [chord]

        context["chords_info"] = chord_things

        ## Recordings created by the user in the display (show-off time!)
        recordings = []
        for r in Recording.objects.all():
            if r.user == userInfo.user:
                recordings += [[r, UserInfo.objects.get(user=r.user), r.date]]

        context["recordings"] = recordings

        return context