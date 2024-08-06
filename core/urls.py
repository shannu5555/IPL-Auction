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
from django.contrib import admin

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
    login_page,register,logout_page,abc,select_teams, match_preview,select_players_to_play,like_post,dislike_post,showerror,aaa,
    match_preview,initial_players,player_detail,x_selectteam,x_selectplayerstoplay,x_matchpreview,add_venue,all_venues,delete_venue,all_of_teams,all_of_team_details,post_list,add_blog,update_blog,delete_blog,
    y_a,view_all_users,render_players,download_center,download_all_teams, download_team_details,top_10_buys,top_10_runs,add_score,increase_runs,decrease_runs,save_runs,increase_matches_played,decrease_matches_played,save_matches_played,
)

urlpatterns = [
    path('', home, name='home'),
    path('homi/', homi, name='homi'),
    path('admin/', admin.site.urls),
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
     

    path('player_detail/<int:player_id>/', player_detail, name='player_detail'),

    
    path('x_selectteam/',x_selectteam , name='x_selectteam'),
    path('x_selectplayerstoplay/<int:match_id>/',x_selectplayerstoplay , name='x_selectplayerstoplay'),
    path('x_matchpreview/<int:match_id>/',x_matchpreview , name='x_matchpreview'),
    
    
    path('add_venue/', add_venue, name='add_venue'),
    path('all_venues/', all_venues, name='all_venues'),
    path('delete_venue/<int:venue_id>/', delete_venue, name='delete_venue'),
    path('delete_venue/<int:venue_id>/', delete_venue, name='delete_venue'),

    path('all_of_teams/', all_of_teams, name='all_of_teams'),
    path('all_of_team_deatils/<int:team_id>/', all_of_team_details, name='all_of_team_details'),

    path('y_a/<int:match_id>/', y_a, name='y_a'),

    path('view_all_users/', view_all_users, name='view_all_users'),

    path('render_players/', render_players, name='render_players'),
    path('download_center/', download_center, name='download_center'),
    path('download_all_teams/', download_all_teams, name='download_all_teams'),
    path('download_team_details/<str:team_name>/', download_team_details, name='download_team_details'),

    path('top_10_buys/', top_10_buys, name='top_10_buys'),
    path('top_10_runs/', top_10_runs, name='top_10_runs'),
    path('add_score/', add_score, name='add_score'),
   
    path('increase_runs/<int:player_id>/', increase_runs, name='increase_runs'),
    path('decrease_runs/<int:player_id>/', decrease_runs, name='decrease_runs'),
    path('save_runs/<int:player_id>/', save_runs, name='save_runs'),

    path('increase_matches_played/<int:player_id>/',increase_matches_played, name='increase_matches_played'),
    path('decrease_matches_played/<int:player_id>/', decrease_matches_played, name='decrease_matches_played'),
    path('save_matches_played/<int:player_id>/', save_matches_played, name='save_matches_played'),

    path('post_list/', post_list, name='post_list'),
    path('addblog/', add_blog, name='add_blog'),

    path('update_blog/<int:pk>/', update_blog, name='update_blog'),
    path('delete_blog/<int:pk>/', delete_blog, name='delete_blog'),

    path('like/<int:pk>/', like_post, name='like_post'),
    path('dislike/<int:pk>/', dislike_post, name='dislike_post'),

    path('showerror/', showerror, name='showerror'),
    path('aaa/', aaa, name='aaa'),
]

if settings.DEBUG:
    urlpatterns+=static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)

urlpatterns+=staticfiles_urlpatterns()