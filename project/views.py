from django.shortcuts import render, redirect
from django.contrib.auth.mixins import LoginRequiredMixin 
from django.views.generic import TemplateView, ListView, DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.urls import reverse 
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .models import * 
import datetime

import plotly
import plotly.graph_objs as go
from django.shortcuts import render
import requests
from .forms import *

# Create your views here.
# class SearchSongsView(LoginRequiredMixin, ListView):
#     model = Scale
#     template_name = "project/search.html"
#     context_object_name = "scales"
#     paginate_by = 5
#     def get_login_url(self) -> str:
#         return reverse("login_guitar_app") 
    
#     def get_queryset(self):
#         qs = super().get_queryset() #.order_by something
#         if 'scale' in self.request.GET:
#             scale = self.request.GET['scale']
#             qs = qs.filter(scale_name = scale)
#         return qs
    
#     def get_context_data(self, **kwargs):
#         c = super().get_context_data(**kwargs)
#         note_count = dict()

#         for scale in self.get_queryset():
#             notes = [scale.I, scale.II, scale.III, scale.IV, scale.V, scale.VI, scale.VII]
#             for n in notes:
#                 if not n in note_count:
#                     note_count[n] = 1
#                 else:
#                     note_count[n] += 1
        
#         keys = list(note_count.keys())
#         print(keys)
#         values = list(note_count.values())

#         fig = go.Bar(x=keys, y=values)
#         bar_div = plotly.offline.plot({'data': [fig]}, auto_open=False, output_type='div')
#         c["graph"] = bar_div

#         return c

    
class RegistrationView(CreateView):
    template_name = 'project/register.html'
    form_class = UserCreationForm
    def dispatch(self, *args, **kwargs):
        if self.request.POST:
            user_form = UserCreationForm(self.request.POST)
            if not user_form.is_valid():
                print("error!")
                return super().dispatch(*args, **kwargs)
            user = user_form.save()     
            login(self.request, user)

            UserInfo.objects.create(user=user, chords_foreignkeys={'list': []})
            
            return redirect(reverse('search_songs'))
        
        return super().dispatch(*args, **kwargs)

def get_content(product):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(f'https://www.ultimate-guitar.com/search.php?search_type=title&value={product}').text
    return html_content

def get_html(url):
    USER_AGENT = "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/44.0.2403.157 Safari/537.36"
    LANGUAGE = "en-US,en;q=0.5"
    session = requests.Session()
    session.headers['User-Agent'] = USER_AGENT
    session.headers['Accept-Language'] = LANGUAGE
    session.headers['Content-Language'] = LANGUAGE
    html_content = session.get(url).text
    return html_content


scale = ["C", "C#(Db)", "D", "D#(Eb)", "E", "F" ,"F#(Gb)", "G" ,"G#(Ab)", "A" ,"A#(Bb)", "B"]

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
    
tuning = ["E", "A", "D", "G", "B", "E"]

def semitone(note, level):
    ii = scale.index(note)
    while level > 0:
        level -= 1
        if ii == len(scale)-1:
            ii = 0
        else:
            ii += 1
    return scale[ii]

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

def getVersionNumber(s):
    the_string = ""
    for c in reversed(s):
        if c in "1234567890":
            the_string = c + the_string
        else:
            break
    return the_string

def search_songs(request):
    html_content = ""
    contents_baby = ""
    CHORDS = []
    artist_name = ""
    song_name = ""
    song_info = ""
    capo_info = ""
    chords_info = []

    the_artist_image = ""

    url_stuff = []
    url_link = ""

    yt_url = ""
    spotify_url = ""

    ver = ""
    stat= ""

    if 'product' in request.GET or 'learn_song' in request.GET :
        # urls
        product = request.GET.get('product')
        html_content = get_content(product)
        
        key_thing = "https://www.ultimate-guitar.com/static/s3/ugdb/media/cover/artist/"
        see = html_content.count(key_thing)

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

                url_stuff += [[profile_pic,tab_url,song_name_is,artist_name_is, version]]
            except:
                print("DONE")
                break

            html_content = html_content[image_last+5:]
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

        # THE SONG
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

                if song_content[index: index+11] == "revision_id":
                    contents_baby = contents_baby.replace("&quot", "").replace(r'\n', '"\n"').replace(r'\r', '').replace('[tab]', '').replace('[/tab]', '').replace('"', '').replace('&#039;', "'").replace('[ch]', '').replace('[/ch]', '').replace('&rsquo;', "'")[0:] 
                    try:
                        contents_baby = contents_baby[contents_baby.index("content;:;")+10:-4]
                    except:
                        contents_baby = "Unfortunately, this song cannot be accessed currently! Please try another song!"
                        stat = "nope"
                    break

        ## if song is already added
        this_song_exists = Song.objects.filter(score_link=url_link)
        ## continue at **

        for chord in CHORDS:
            lookup = chord.replace("#", "%23")
            chord_content = get_html(f'https://jguitar.com/chordsearch?chordsearch={lookup}')
            image_c = ""
            try:
                ic = chord_content.index("\"/images/chordshape/")
                image_c = chord_content[ic: ic+100]
                image_c = image_c[2:image_c.index("\" alt=")]
            except:
                ""

            audio_c = ""
            try:
                ac = chord_content.index("\"/audio/chordshape/")
                audio_c = chord_content[ac: ac+100]
                audio_c = audio_c[2:audio_c.index("\" title=")]
            except:
                ""
            
            if not image_c == "" and not audio_c == "" and ".png" in image_c and (not "{" in image_c or not "(" in image_c):
                chords_info += [["https://jguitar.com/" + image_c, "https://jguitar.com/" + audio_c, find_notes_string(image_c), lookup.replace("%23", "#")]]

        # youtube thing 
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

        if yt_url == "": # try again
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


        # Add song
        if  "add_song" in request.POST and not(song_name == "") and len(contents_baby) > 100:
            artistName = artist_name
            artist_list = Artist.objects.filter(name=artistName)
            capo = -1
            if not capo_info == "":
                cp = capo_info.split(" ")
                if cp[1][0] in "1234567890":
                    capo = int(cp[1])

            if 'csrfmiddlewaretoken' in request.POST:
                yt_url = ""

            vl = ""
            if not yt_url == "":
                vl = yt_url

            if list(artist_list) == []:
                Artist.objects.create(name=artistName, image_url=the_artist_image)
                artist_list = Artist.objects.filter(name=artistName)
            
            song_list = Song.objects.filter(score_link = url_link)

            if list(song_list) == []:
                hi = Song.objects.create(chords_foreignkeys = {"list": CHORDS}, 
                                        lyrics=contents_baby, 
                                        score_link = url_link, 
                                        artist = artist_list[0], 
                                        song_name = song_name, 
                                        users_and_their_progresses = {"list": [ [request.user.pk, False] ]}, 
                                        capo_info = capo, additional_info = song_info, 
                                        spotify_link=spotify_url, 
                                        vimeo_link = vl)
            
                print("Song " + str(hi) + " created")
            elif not list(this_song_exists) == []:
                the_song = list(this_song_exists)[0]
                users_from_song = the_song.users_and_their_progresses["list"]
                users_from_song += [[request.user.pk, False]]
                Song.objects.filter(score_link=url_link).update(users_and_their_progresses = {"list": users_from_song})

            # Add chords
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
    
        if 'csrfmiddlewaretoken' in request.POST :
            yt_url = ""

        ## **
        if not list(this_song_exists) == []:
            users_from_song = list(this_song_exists)[0].users_and_their_progresses["list"]
            for l in users_from_song:
                if l[0] == request.user.pk:
                    stat = "already added"
                    print("ALREADY ADDED")
                    break
    if 'csrfmiddlewaretoken' in request.POST :
        print("Message detected!")
        yt_url = ""
    
    print("vimeo link? ", yt_url)

    return render( request, "project/search_songs.html", {'lyrics': contents_baby, "artist_name" : artist_name, "chords": CHORDS, "song_name": song_name, "chords_info": chords_info, "song_info": song_info, "the_artist_image": the_artist_image, "url_stuff": url_stuff, "url_link": url_link, "spotify_url": spotify_url, "item": yt_url, "capo_stuff": capo_info, "ver": ver, "status": stat})








# normal views:
class ShowAllArtists(ListView):
    model = Artist
    template_name = "project/show_all_artists.html"
    context_object_name = "artists"

class ShowAllChords(ListView):
    model = Chord
    template_name = "project/show_all_chords.html"
    context_object_name = "chords"

class ShowAllSongs(ListView):
    model = Song
    template_name = "project/show_all_songs.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        songs = []
        for song in Song.objects.all().order_by('song_name'):
            songs += [[song, getVersionNumber(song.score_link)]]
        context["songs"] = songs
        return context
    
class ShowAllUsers(ListView):
    model = UserInfo
    template_name = "project/show_all_users.html"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        users = []
        for ui in UserInfo.objects.all():
            songs_learned = 0
            songs_learning = 0
            chords_learned = len(ui.chords_foreignkeys["list"])
            recordings = 0
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
            
            users += [[ui, songs_learned,songs_learning,chords_learned,recordings]]

        context["users"] = users
        return context

class ShowSong(DetailView):
    model = Song
    template_name = "project/song.html"
    context_object_name = "s"

    def post(self, request, *args, **kwargs):
        if "learned_this_song" in request.POST:
            song = Song.objects.get(pk=self.kwargs['pk'])
            u_a_p = song.users_and_their_progresses["list"]
            for i in range(len(u_a_p)):
                l = u_a_p[i]
                if l[0] == self.request.user.pk:
                    u_a_p[i][1] = True
                    break
            Song.objects.filter(pk=self.kwargs['pk']).update(users_and_their_progresses={"list": u_a_p})
            print("HEYYYy", u_a_p)
        if "add_this_song_to_learn" in request.POST:
            song = Song.objects.get(pk=self.kwargs['pk'])
            l = song.users_and_their_progresses["list"]
            l += [[self.request.user.pk, False]]
            Song.objects.filter(pk=self.kwargs['pk']).update(users_and_their_progresses= {"list": l})
            
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'

        if is_ajax:
            audio_file = request.FILES.get('recorded_audio')
            print("RECORDING DONE.")
            song = Song.objects.get(pk=self.kwargs['pk'])
            Recording.objects.create(audio = audio_file, user= request.user,song=song)

        return redirect(reverse('song', kwargs = {'pk':self.kwargs['pk']})) 

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        song = Song.objects.get(pk=self.kwargs['pk'])
        songName = song.song_name
        users_and_prog = song.users_and_their_progresses["list"]
        context["artist"] = song.artist
        chs = song.chords_foreignkeys["list"]
        context["chords"] = chs
        context["item"] = song.vimeo_link 

        chord_things = []

        learned_chords = []
        if self.request.user.is_authenticated:
            learned_chords = UserInfo.objects.get(user=self.request.user).chords_foreignkeys["list"]

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
            if r.song.song_name == songName:
                recordings += [[r, UserInfo.objects.get(user=r.user)]]

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
    
keyboard = ["E", "F" ,"F#(Gb)", "G" ,"G#(Ab)", "A" ,"A#(Bb)", "B", "C", "C#(Db)", "D", "D#(Eb)", "E", "F" ,"F#(Gb)", "G" ,"G#(Ab)", "A" ,"A#(Bb)", "B","C", "C#(Db)", "D", "D#(Eb)", "E", "F" ,"F#(Gb)", "G" ,"G#(Ab)", "A" ,"A#(Bb)", "B", "C", "C#(Db)", "D", "D#(Eb)", "E", "F" ,"F#(Gb)", "G" ,"G#(Ab)", "A" ,"A#(Bb)", "B", "C", "C#(Db)", "D", "D#(Eb)", "E", "F" ,"F#(Gb)", "G" ,"G#(Ab)", "A" ,"A#(Bb)", "B"]
n_files = ["-e", "-f" ,"-fs", "-g" ,"-gs", "-a" ,"-as", "-b", "-c", "-cs", "-d", "-ds", "-e", "-f" ,"-fs", "-g" ,"-gs", "-a" ,"-as", "-b","-c", "-cs", "-d", "-ds", "-e", "-f" ,"-fs", "-g" ,"-gs", "-a" ,"-as", "-b", "-c", "-cs", "-d", "-ds", "-e", "-f" ,"-fs", "-g" ,"-gs", "-a" ,"-as", "-b", "-c", "-cs", "-d", "-ds", "-e", "-f" ,"-fs", "-g" ,"-gs", "-a" ,"-as", "-b"]

class ShowChord(DetailView):
    model = Chord
    template_name = "project/chord.html"
    context_object_name = "c"

    def post(self, request, *args, **kwargs):
        is_ajax = request.headers.get('X-Requested-With') == 'XMLHttpRequest'
        chord = Chord.objects.get(pk=self.kwargs['pk'])
        chordName = chord.chord_name

        if is_ajax:
            userInfo = UserInfo.objects.get(user=self.request.user)
            learned_chords = userInfo.chords_foreignkeys["list"]
            learned_chords += [chordName]
            UserInfo.objects.filter(user=self.request.user).update(chords_foreignkeys = {"list": learned_chords})

        return redirect(reverse('song', kwargs = {'pk':self.kwargs['pk']})) 
        
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        chord = Chord.objects.get(pk=self.kwargs['pk'])
        context["lookup_more"] = "https://jguitar.com/chordsearch?chordsearch=" + chord.chord_name
        chordNotes = chord.notes["list"]
        context["chords"] = chordNotes
        instructions = []
        media_notes = []
        ii = 0
        level = 2
        j = -1
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

        ## related songs
        chordName = chord.chord_name
        related_songs = []
        for song in Song.objects.all():
            chordsList = song.chords_foreignkeys["list"]
            if chordName in chordsList:
                related_songs += [[song.song_name, song.artist.name, getVersionNumber(song.score_link), song.artist.image_url, song.pk]]
                print(song.pk)
        context["related_songs"] = related_songs

        ## learned it or not
        learn = ""
        if self.request.user.is_authenticated:
            userInfo = UserInfo.objects.get(user=self.request.user)
            if chordName in userInfo.chords_foreignkeys["list"]:
                learn = "user_learned"
            else:
                learn = "user_hasnt"
        
        context["learn"] = learn

        return context
    

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
            return redirect(reverse('show_all_artists')) 
        
    def get_success_url(self):
        return reverse("show_all_artists")
    
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
        fig = go.Bar(x=x, y=y)
        bar_div = plotly.offline.plot({'data': [fig]},
                                      auto_open=False,
                                      output_type='div',)
        
        context['bar_div'] = bar_div
        context["songs"] = songs
        context["song_count"] = len(songs)


        return context






## User stuff
class ShowUserInfo(DetailView):
    model = UserInfo
    template_name = "project/show_userinfo.html"
    context_object_name = "ui"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        userInfo = UserInfo.objects.get(pk=self.kwargs['pk'])
        songs_in_progress = []
        for song in Song.objects.all():
            for l in song.users_and_their_progresses["list"]:
                if l[0] == userInfo.user.pk and not l[1]:
                    songs_in_progress += [[song, getVersionNumber(song.score_link)]]
        context["songs_in_progress"] = songs_in_progress
        return context