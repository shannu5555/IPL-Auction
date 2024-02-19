"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings

from django.conf.urls.static import static
from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns

from django.conf.urls.static import static
from iplauction.views import (
    home,
    create_team,
    all_teams,
    add_player,
    all_players,
    auction_page,
    bid_player,
    sold_players,
    team_details,
    delete_player,
    delete_team,
    homi,
    login_page,register,logout_page,abc,select_teams, match_preview,select_players_to_play,
    match_preview,initial_players,
)

urlpatterns = [
    path('', home, name='home'),
    path('homi/', homi, name='homi'),
    
    path('abc/', abc, name='abc'),
    path('create_team/', create_team, name='create_team'),
    path('all_teams/', all_teams, name='all_teams'),
    path('add_player/', add_player, name='add_player'),
    path('all_players/', all_players, name='all_players'),
    path('auction/', auction_page, name='auction_page'),
    path('bid_player/', bid_player, name='bid_player'),
    path('sold_players/', sold_players, name='sold_players'),
    path('team_details/<str:team_name>/', team_details, name='team_details'),
    path('delete_player/<int:player_id>/', delete_player, name='delete_player'),
    path('delete_team/<int:team_id>/', delete_team, name='delete_team'),
    path('login/', login_page,name="login_page"),
    path('register/', register,name="register"),
    path('logout/',logout_page,name="logout_page"),

    path('selectteams/', select_teams, name='select_teams'),
    path('select_players_to_play/<int:match_id>/', select_players_to_play, name='select_players_to_play'),
    path('match_preview/<int:match_id>/', match_preview, name='match_preview'),
     path('initial_players/', initial_players, name='initial_players'),
     



    
    
    
    
    

    
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns+=staticfiles_urlpatterns()