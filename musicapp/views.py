from django.shortcuts import render, redirect
from .models import *
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import cv2
from deepface import DeepFace
import numpy as np


def index(request):
    if not request.user.is_anonymous:
        recent = list(Recent.objects.filter(
            user=request.user).values('song_id').order_by('song_id'))
        recent_id = [each['song_id'] for each in recent][:7]
        recent_songs_unsorted = Song.objects.filter(
            song_id__in=recent_id, recent__user=request.user)
        recent_songs = list()
        for song_id in recent_id:
            recent_songs.append(recent_songs_unsorted.get(song_id=song_id))
    else:
        recent = None
        recent_songs = None

    first_time = False

    if not request.user.is_anonymous:
        last_played_list = list(Recent.objects.filter(
            user=request.user).values('song_id').order_by('song_id'))
        if last_played_list:
            last_played_id = last_played_list[0]['song_id']
            last_played_song = Song.objects.get(song_id=last_played_id)
        else:
            first_time = True
            last_played_song = Song.objects.get(song_id=7)

    else:
        first_time = True
        last_played_song = Song.objects.get(song_id=7)

    song = Song.objects.all()

    songs_english = list(Song.objects.filter(
        language='English').values('song_id'))
    sliced_ids = [each['song_id'] for each in songs_english][:6]
    indexpage_english_songs = Song.objects.filter(song_id__in=sliced_ids)

    songs_hindi = list(Song.objects.filter(language='Hindi').values('song_id'))
    sliced_ids = [each['song_id'] for each in songs_hindi][:6]
    indexpage_hindi_songs = Song.objects.filter(song_id__in=sliced_ids)

    songs_all = list(Song.objects.all().values('song_id').order_by('?'))
    sliced_ids = [each['song_id'] for each in songs_all][:6]
    indexpage_songs = Song.objects.filter(song_id__in=sliced_ids)

    context = {'all_songs': indexpage_songs,
               'recent_songs': recent_songs,
               'hindi_songs': indexpage_hindi_songs,
               'english_songs': indexpage_english_songs,
               'last_played': last_played_song,
               'first_time': first_time,
               }
    return render(request, 'musicapp/index.html', context=context)


def english_songs(request):

    english_songs = Song.objects.filter(language='English')
    last_played_list = list(Recent.objects.values(
        'song_id').order_by('song_id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(song_id=last_played_id)
    else:
        last_played_song = Song.objects.get(song_id=7)

    query = request.GET.get('q')

    if query:
        english_songs = Song.objects.filter(
            Q(name__icontains=query)).distinct()
        context = {'english_songs': english_songs}
        return render(request, 'musicapp/english_songs.html', context)

    context = {'english_songs': english_songs, 'last_played': last_played_song}
    return render(request, 'musicapp/english_songs.html', context=context)


def happy_song(request):

    happy_song = Song.objects.filter(mood='Happy')
    return render(request, 'musicapp/happy_song.html', {'happy_song': happy_song})


def sad_song(request):
    sad_song = Song.objects.filter(mood='Sad')
    context = {'sad_song': sad_song}
    return render(request, 'musicapp/sad_song.html', context)


def neutral_song(request):
    neutral_song = Song.objects.filter(mood='Neutral')
    last_played_list = list(Recent.objects.values(
        'song_id').order_by('song_id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(song_id=last_played_id)
    else:
        last_played_song = Song.objects.get(song_id=7)
    context = {'neutral_song': neutral_song,  'last_played': last_played_song}
    return render(request, 'musicapp/neutral_song.html', context)


def angry_song(request):
    angry_song = Song.objects.filter(mood='Angry')
    last_played_list = list(Recent.objects.values(
        'song_id').order_by('song_id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(song_id=last_played_id)
    else:
        last_played_song = Song.objects.get(song_id=7)
    context = {'angry_song': angry_song,  'last_played': last_played_song}
    return render(request, 'musicapp/angry_song.html', context)


def fear_song(request):
    fear_song = Song.objects.filter(mood='Fear')
    last_played_list = list(Recent.objects.values(
        'song_id').order_by('song_id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(song_id=last_played_id)
    else:
        last_played_song = Song.objects.get(song_id=7)
    context = {'fear_song': fear_song,  'last_played': last_played_song}
    return render(request, 'musicapp/fear_song.html', context)


def hindi_songs(request):

    hindi_songs = Song.objects.filter(language='Hindi')
    last_played_list = list(Recent.objects.values(
        'song_id').order_by('song_id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(song_id=last_played_id)
    else:
        last_played_song = Song.objects.get(song_id=7)

    query = request.GET.get('q')

    if query:
        hindi_songs = Song.objects.filter(Q(name__icontains=query)).distinct()
        context = {'hindi_songs': hindi_songs}
        return render(request, 'musicapp/hindi_songs.html', context)

    context = {'hindi_songs': hindi_songs, 'last_played': last_played_song}
    return render(request, 'musicapp/hindi_songs.html', context=context)


@login_required(login_url='login')
def play_song(request, id):
    songs = Song.objects.filter(song_id=id).first()
    if list(Recent.objects.filter(song=songs, user=request.user).values()):
        data = Recent.objects.filter(song=songs, user=request.user)
        data.delete()
    data = Recent(song=songs, user=request.user)
    data.save()
    return redirect('all_songs')


@login_required(login_url='login')
def play_song_index(request, id):
    songs = Song.objects.filter(song_id=id).first()
    if list(Recent.objects.filter(song=songs, user=request.user).values()):
        data = Recent.objects.filter(song=songs, user=request.user)
        data.delete()
    data = Recent(song=songs, user=request.user)
    data.save()
    return redirect('index')


@login_required(login_url='login')
def play_recent_song(request, id):
    songs = Song.objects.filter(song_id=id).first()
    # Add data to recent database
    if list(Recent.objects.filter(song=songs, user=request.user).values()):
        data = Recent.objects.filter(song=songs, user=request.user)
        data.delete()
    data = Recent(song=songs, user=request.user)
    data.save()
    return redirect('recent')


@login_required(login_url='login')
def allsong(request):
    songs = Song.objects.all()

    first_time = False
    if not request.user.is_anonymous:
        last_played_list = list(Recent.objects.filter(
            user=request.user).values('song_id').order_by('song_id'))
        if last_played_list:
            last_played_id = last_played_list[0]['song_id']
            last_played_song = Song.objects.get(song_id=last_played_id)
    else:
        first_time = True
        last_played_song = Song.objects.get(song_id=7)

    qs_artists = Song.objects.values_list('artist').all()
    a_list = [a.split(',') for artist in qs_artists for a in artist]
    all_artist = sorted(
        list(set([a.strip() for artist in a_list for a in artist])))
    qs_languages = Song.objects.values_list('language').all()
    all_languages = sorted(
        list(set([l.strip() for lang in qs_languages for l in lang])))

    if len(request.GET) > 0:
        search_query = request.GET.get('q')
        search_artist = request.GET.get('artists') or ''
        search_language = request.GET.get('languages') or ''
        filtered_songs = songs.filter(Q(name__icontains=search_query)).filter(
            Q(language__icontains=search_language)).filter(Q(artist__icontains=search_artist)).distinct()
        context = {
            'songs': filtered_songs,
            'last_played': last_played_song,
            'all_artist': all_artist,
            'all_languages': all_languages,
            'query_search': True,
        }
        return render(request, 'musicapp/all_songs.html', context)

    context = {
        'songs': songs,
        'last_played': last_played_song,
        'first_time': first_time,
        'all_artist': all_artist,
        'all_languages': all_languages,
        'query_search': False,
    }
    return render(request, 'musicapp/all_songs.html', context=context)


def recent(request):
    last_played_list = list(Recent.objects.values(
        'song_id').order_by('song_id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(song_id=last_played_id)
    else:
        last_played_song = Song.objects.get(song_id=7)
    recent = list(Recent.objects.filter(
        user=request.user).values('song_id').order_by('song_id'))
    recent_id = [each['song_id'] for each in recent][:6]
    recent_songs_unsorted = Song.objects.filter(
        song_id__in=recent_id, recent__user=request.user)
    recent_songs = list()
    for song_id in recent_id:
        recent_songs.append(recent_songs_unsorted.get(song_id=song_id))
    else:
        recent = None
        recent_songs = None

    context = {'recent_songs': recent_songs, 'last_played': last_played_song, }
    return render(request, 'musicapp/recent.html', context=context)


@login_required(login_url='login')
def player(request, id):
    songs = Song.objects.filter(song_id=id).first()
    if list(Recent.objects.filter(song=songs, user=request.user).values()):
        data = Recent.objects.filter(song=songs, user=request.user)
        data.delete()
    data = Recent(song=songs, user=request.user)
    data.save()
    last_played_list = list(Recent.objects.values(
        'song_id').order_by('song_id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(song_id=last_played_id)
    else:
        last_played_song = Song.objects.get(song_id=7)

    playlists = Playlist.objects.filter(
        user=request.user).values('playlist_name').distinct
    is_favourite = Favourite.objects.filter(
        user=request.user).filter(song=id).values('is_fav')

    if request.method == "POST":
        if 'playlist' in request.POST:
            playlist_name = request.POST["playlist"]
            q = Playlist(user=request.user, song=songs,
                         playlist_name=playlist_name)
            q.save()
            messages.success(request, "Song added to playlist!")
        elif 'add-fav' in request.POST:
            is_fav = True
            query = Favourite(user=request.user, song=songs, is_fav=is_fav)
            print(f'query: {query}')
            query.save()
            messages.success(request, "Added to favorite!")
            return redirect('player', id=id)
        elif 'rm-fav' in request.POST:
            is_fav = True
            query = Favourite.objects.filter(
                user=request.user, song=songs, is_fav=is_fav)
            print(f'user: {request.user}')
            print(f'song: {songs.song_id} - {songs}')
            print(f'query: {query}')
            query.delete()
            messages.success(request, "Removed from favorite!")
            return redirect('player', id=id)

    context = {'songs': songs, 'playlists': playlists,
               'is_favourite': is_favourite, 'last_played': last_played_song}
    return render(request, 'musicapp/player.html', context=context)


@login_required(login_url='login')
def detail(request, id):
    songs = Song.objects.filter(song_id=id).first()

    if list(Recent.objects.filter(song=songs, user=request.user).values()):
        data = Recent.objects.filter(song=songs, user=request.user)
        data.delete()
    data = Recent(song=songs, user=request.user)
    data.save()
    last_played_list = list(Recent.objects.values(
        'song_id').order_by('song_id'))
    if last_played_list:
        last_played_id = last_played_list[0]['song_id']
        last_played_song = Song.objects.get(song_id=last_played_id)
    else:
        last_played_song = Song.objects.get(song_id=7)

    playlists = Playlist.objects.filter(
        user=request.user).values('playlist_name').distinct
    is_favourite = Favourite.objects.filter(
        user=request.user).filter(song=id).values('is_fav')

    if request.method == "POST":

        if 'playlist' in request.POST:

            playlist_name = request.POST["playlist"]
            query = Playlist(user=request.user, song=songs,
                             playlist_name=playlist_name)
            query.save()
            messages.success(request, "Song added to playlist!")
        elif 'add-fav' in request.POST:
            is_fav = True
            query = Favourite(user=request.user, song=songs, is_fav=is_fav)
            print(f'query: {query}')
            query.save()
            messages.success(request, "Added to favorite!")
            return redirect('detail', id=id)
        elif 'rm-fav' in request.POST:
            is_fav = True
            query = Favourite.objects.filter(
                user=request.user, song=songs, is_fav=is_fav)
            print(f'user: {request.user}')
            print(f'song: {songs.song_id} - {songs}')
            print(f'query: {query}')
            query.delete()
            messages.success(request, "Removed from favorite!")
            return redirect('detail', id=id)

    context = {'songs': songs, 'playlists': playlists,
               'is_favourite': is_favourite, 'last_played': last_played_song}
    return render(request, 'musicapp/detail.html', context=context)


@login_required(login_url='login')
def search(request):
    songs = Song.objects.all()
    if len(request.GET) > 0:
        search_query = request.GET.get('q')
        filtered_songs = songs.filter(Q(name__icontains=search_query))
        context = {
            'songs': filtered_songs,
            'query_search': True,
        }
        return render(request, 'musicapp/search.html', context)

    context = {
        'songs': songs,
        'query_search': False,
    }
    return render(request, 'musicapp/search.html', context=context)


def playlist(request):
    playlists = Playlist.objects.filter(
        user=request.user).values('playlist_name').distinct()

    context = {'playlists': playlists}
    return render(request, 'musicapp/playlist.html', context=context)


def playlist_songs(request, playlist_name):
    songs = Song.objects.filter(
        playlist__playlist_name=playlist_name, playlist__user=request.user).distinct()

    if request.method == "POST":
        song_id = list(request.POST.keys())[1]
        playlist_song = Playlist.objects.filter(
            playlist_name=playlist_name, song__id=song_id, user=request.user)
        playlist_song.delete()
        messages.success(request, "Song removed from playlist!")

    context = {'playlist_name': playlist_name, 'songs': songs}

    return render(request, 'musicapp/playlist_songs.html', context=context)


def favourite(request):
    songs = Song.objects.filter(
        favourite__user=request.user, favourite__is_fav=True).distinct()
    print(f'songs: {songs}')

    if request.method == "POST":

        song_id = list(request.POST.keys())[1]
        favourite_song = Favourite.objects.filter(
            user=request.user, song__id=song_id, is_fav=True)
        favourite_song.delete()
        messages.success(request, "Removed from favourite!")
    context = {'songs': songs}
    return render(request, 'musicapp/fav.html', context=context)


@login_required(login_url='login')
def mymusic(request):
    return render(request, 'musicapp/mymusic.html')


@login_required(login_url='login')
def cam(request):
    return render(request, 'musicapp/camera.html')

def mooddet(request):
    exp = ['happy', 'sad', 'neutral', 'fear', 'angry']
    facecascade = cv2.CascadeClassifier(
        cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

    cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

    while True:
        ret, frame = cap.read()
        result = DeepFace.analyze(frame, actions=['emotion'], enforce_detection=False)

        if len(result) > 0:
            emotion = result[0]['dominant_emotion']

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            faces = facecascade.detectMultiScale(frame, 1.1, 5)

            for (x, y, w, h) in faces:
                cv2.rectangle(frame, (x, y), (x+w, y+h), (255, 0, 0), 3)

            font = cv2.FONT_HERSHEY_SIMPLEX

            cv2.putText(frame, emotion, (50, 50), font, 1, (220, 220, 220), 2, cv2.LINE_4)

            cv2.imshow('Capturing', frame)
            print(emotion)
        key = cv2.waitKey(1)
        if key == ord('r'):
            if emotion == 'happy':
                cap.release()
                cv2.destroyAllWindows()
                happy_song = Song.objects.filter(mood='Happy')
                context = {'happy_song': happy_song}
                return render(request, 'musicapp/happy_song.html', context)
            elif emotion == 'sad':
                cap.release()
                cv2.destroyAllWindows()
                sad_song = Song.objects.filter(mood='Sad')
                context = {'sad_song': sad_song}
                return render(request, 'musicapp/sad_song.html', context)
            elif emotion == 'neutral':
                cap.release()
                cv2.destroyAllWindows()
                neutral_song = Song.objects.filter(mood='Neutral')
                context = {'neutral_song': neutral_song}
                return render(request, 'musicapp/neutral_song.html', context)
            elif emotion == 'fear':
                cap.release()
                cv2.destroyAllWindows()
                fear_song = Song.objects.filter(mood='Fear')
                context = {'fear_song': fear_song}
                return render(request, 'musicapp/fear_song.html', context)
            elif emotion == 'angry':
                cap.release()
                cv2.destroyAllWindows()
                angry_song = Song.objects.filter(mood='Angry')
                context = {'angry_song': angry_song}
                return render(request, 'musicapp/angry_song.html', context)

        elif key == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            break
    return render(request, 'musicapp/camera.html')
