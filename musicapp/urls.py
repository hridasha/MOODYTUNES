from django.urls import path
from . import views

# Add URLConf
urlpatterns = [

     path('', views.index, name='index'),
     path('<int:id>/', views.detail, name='detail'),
     path('player/<int:id>/', views.player, name='player'),
     path('mymusic/', views.mymusic, name='mymusic'),
     path('playlist/', views.playlist, name='playlist'),
     path('playlist/<str:playlist_name>/',
          views.playlist_songs, name='playlist_songs'),
     path('favourite/', views.favourite, name='favourite'),
     path('recent/', views.recent, name='recent'),
     path('hindi_songs/', views.hindi_songs, name='hindi_songs'),
     path('result/', views.happy_song, name='happy_song'),
     path('english_songs/', views.english_songs, name='english_songs'),
     path('play/<int:id>/', views.play_song, name='play_song'),
     path('play_song/<int:id>/', views.play_song_index, name='play_song_index'),
     path('play_recent_song/<int:id>/',
          views.play_recent_song, name='play_recent_song'),
     path('allsong/', views.allsong, name='allsong'),
     path('search/', views.search, name='search'),
     path('cam/', views.cam, name="cam"),
     path('mooddet/', views.mooddet, name="mooddet"),
     path('happy_song/', views.happy_song, name="happy_song"),
     path('sad_song/', views.sad_song, name="sad_song"),
     path('neutral_song/', views.neutral_song, name="neutral_song"),
     path('angry_song/', views.angry_song, name="angry_song"),
     path('fear_song/', views.fear_song, name="fear_song"),
]
