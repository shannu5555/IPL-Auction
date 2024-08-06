# auction/views.py
from django.shortcuts import render, redirect
from .models import Team, Player, Bid ,Match ,Venue
from .forms import CreateTeamForm, AddPlayerForm
from django.shortcuts import get_object_or_404
from django.db.models import Sum
from django.db.models import Max

from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate
from django.contrib.auth import login,logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404

from django.db.models import Q
from .forms import VenueForm
from django.contrib.auth.models import User
from django.http import HttpResponse
import xlwt
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseServerError


def render_players(request):
    players_names = Player.objects.all().values_list('name', flat=True) 
    id_values = Player.objects.all().values_list('id', flat=True)  
    runs = Player.objects.all().values_list('runs_scored', flat=True)  
    matches = Player.objects.all().values_list('matches_played', flat=True)
    wickets = Player.objects.all().values_list('wickets_taken', flat=True)
    dob = Player.objects.all().values_list('dob', flat=True)
    batting_style = Player.objects.all().values_list('batting_style', flat=True)
    player_type = Player.objects.all().values_list('playertype', flat=True)  
    base_price = Player.objects.all().values_list('base_price', flat=True)
    country = Player.objects.all().values_list('international_team_name', flat=True)
    
    #EXCL
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="players.xls"'

    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('Players')

   
    style_heading = xlwt.easyxf('font: bold on, color white; pattern: pattern solid, fore_colour dark_blue;')
    style1 = xlwt.easyxf('pattern: pattern solid, fore_colour light_blue;')
    style2 = xlwt.easyxf('pattern: pattern solid, fore_colour light_yellow;')

 
    headings = ['Player Name', 'ID', 'Runs Scored', 'Matches', 'Wickets', 'DOB', 'Batting Style', 'Player Type', 'BasePrice', 'Country']
    for col, heading in enumerate(headings):
        worksheet.write(0, col, heading, style_heading)

   
    styles = [style1, style2]
    for row, data in enumerate(zip(players_names, id_values, runs, matches, wickets, dob, batting_style, player_type, base_price, country), start=1):
        for col, value in enumerate(data):
            worksheet.write(row, col, value, styles[row % 2])  # Apply alternating styles

    workbook.save(response)
    return response



def download_all_teams(request):
    teams = Team.objects.all()
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = 'attachment; filename="all_teams.xls"'
    
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet('All Teams')
    
    # Writing headings
    worksheet.write(0, 0, 'Team Name')
    worksheet.write(0, 1, 'Amount')
    worksheet.write(0, 2, 'Total Amount Spent')

    for row, team in enumerate(teams, start=1):
        worksheet.write(row, 0, team.name)  # Assuming team.name is a string
        worksheet.write(row, 1, team.amount) # Convert amount to string if necessary
        worksheet.write(row, 2, team.total_amount_spent())  # Convert to string if necessary
    # Convert to string if necessary


    workbook.save(response)
    return response

def download_team_details(request):
    teams = Team.objects.all()
    team_name = request.GET.get('team_name')
    team = Team.objects.get(name=team_name)
    players = Bid.objects.filter(bidder=team)
    
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{team_name}_details.xls"'
    
    workbook = xlwt.Workbook(encoding='utf-8')
    worksheet = workbook.add_sheet(f'{team_name} Details')
    
    # Writing headings
    worksheet.write(0, 0, 'Player Name')
    worksheet.write(0, 1, 'Base Price')
    worksheet.write(0, 2, 'Amount')
    worksheet.write(0, 3, 'Player Type')
    worksheet.write(0, 4, 'ID')

    for row, player in enumerate(players, start=1):
        worksheet.write(row, 0, player.player.name)
        worksheet.write(row, 1, player.player.base_price)
        worksheet.write(row, 2, player.amount)
        worksheet.write(row, 3, player.player.playertype)
        worksheet.write(row, 4, player.player.id)

    workbook.save(response)
    return response


def download_center(request):
    return render(request, 'download_center.html')

def showerror(request):
    return render(request, 'showerror.html')

def view_all_users(request):
    users = User.objects.all()
    return render(request, 'view_all_users.html', {'users': users})

@login_required(login_url="/login/")
def home(request):
    posts = Post.objects.all()
    players = Player.objects.all() 
    sorted_players_runs = sorted(players, key=lambda x: x.runs_scored, reverse=True)
    sorted_players_wickets=sorted(players, key=lambda x: x.wickets_taken, reverse=True)
    sorted_players_average_runs = sorted(players, key=lambda x: x.average_runs_per_match(), reverse=True)
    top_average_runs_player = sorted_players_average_runs[:1]


    sold_players = Bid.objects.filter(amount__gt=0)
    sorted_sold_players_top = sorted(sold_players, key=lambda x: x.amount, reverse=True)
    top_sold_player = sorted_sold_players_top[:1]
    top_run_scorer = sorted_players_runs[:1]
    top_wicket_taker=sorted_players_wickets[:1]
    
    return render(request, 'home.html',{'posts':posts,'top_run_scorer':top_run_scorer,'top_sold_player':top_sold_player,'top_wicket_taker':top_wicket_taker,'top_average_runs_player': top_average_runs_player,})

def x(request):
    return render(request, 'x.html')

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
def aaa(request):
    # Retrieve all players
    players = Player.objects.all()

    # Pagination
    paginator = Paginator(players, 1)  # Change '1' to the number of players per page
    page_number = request.GET.get('page')
    try:
        players_page = paginator.page(page_number)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        players_page = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        players_page = paginator.page(paginator.num_pages)

    return render(request, 'aaa.html', {'players_page': players_page})

def abc(request):
    teams = Team.objects.all()

    team_data = []
    for team in teams:
        batsmen_count = Bid.objects.filter(bidder=team, player__playertype='Batsmen').count()
        bowler_count = Bid.objects.filter(bidder=team, player__playertype='Bowler').count()
        allrounder_count = Bid.objects.filter(bidder=team, player__playertype='Allrounder').count()
        pname=Bid.objects.filter(bidder=team,player__name='T Head').count()
        batsmen_players = Bid.objects.filter(bidder=team, player__playertype='Batsmen').values_list('player__name', flat=True)
        bowler_players = Bid.objects.filter(bidder=team, player__playertype='Bowler').values_list('player__name', flat=True)
        allrounder_players = Bid.objects.filter(bidder=team, player__playertype='Allrounder').values_list('player__name', flat=True)

        team_data.append({
            'team': team,
            'batsmen_count': batsmen_count,
            'bowler_count': bowler_count,
            'allrounder_count': allrounder_count,
            'pname':pname,
            'batsmen_players':batsmen_players ,
            'bowler_players':bowler_players,
            'allrounder_players':allrounder_players,

            
        })

    context = {'team_data': team_data}
    return render(request, 'abc.html', context)
    

@login_required(login_url="/login/")
def homi(request):
    
    return render(request, 'homi.html')

@login_required(login_url="/login/")
def create_team(request):
    if request.method == 'POST':
        form = CreateTeamForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all_teams')
    else:
        form = CreateTeamForm()
    return render(request, 'add_team.html', {'form': form})

@login_required(login_url="/login/")
def all_teams(request):
    teams = Team.objects.all()

    return render(request, 'all_team.html', {'teams': teams})

@login_required(login_url="/login/")
def team_details(request, team_name):
    team = Team.objects.get(name=team_name)
    players = Bid.objects.filter(bidder=team)
    team_amount = team.amount
    teams = Team.objects.all() 
    return render(request, 'team_details.html', {'team': team, 'players': players, 'team_amount': team_amount,'teams': teams})

@login_required(login_url="/login/")
def add_player(request):
    if request.method == 'POST':
        form = AddPlayerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all_players')
    else:
        form = AddPlayerForm()
    return render(request, 'add_player.html', {'form': form})

@login_required(login_url="/login/")
def all_players(request):
    players = Player.objects.all()
    sorted_players = sorted(players, key=lambda x: x.runs_scored, reverse=True)

   
    top_10_players = sorted_players[:10]
    return render(request, 'all_player.html', {'players': players,'top_10_players':top_10_players})


@login_required(login_url="/login/")
def auction_page(request):
    players = Player.objects.filter(bid__isnull=True)
    live_bidding_amount = get_live_bidding_amount()
    last_bids = get_last_bids()

    team_amounts = Team.objects.annotate(total_amount_spent=Sum('bid__amount'))

    
    return render(request, 'auction.html', {
        'players': players,
        'live_bidding_amount': live_bidding_amount,
        'last_bids': last_bids,
        'teams': Team.objects.all(), 
    })

@login_required(login_url="/login/")
def bid_player(request):
    if request.method == 'POST':
        player_id = request.POST.get('player_id')
        bidder_name = request.POST.get('bidder')
        amount = request.POST.get('amount')

        player = Player.objects.get(pk=player_id)
        bidder = Team.objects.get(name=bidder_name)

        bid = Bid(player=player, bidder=bidder, amount=amount)
        bid.save()

        return redirect('auction_page')


def get_live_bidding_amount():
    
    return 0

def get_last_bids():
    
    return Bid.objects.filter(amount__gt=0).order_by('-id')[:5] 

@login_required(login_url="/login/")
def sold_players(request):
    search_query = request.GET.get('search', '')
    sold_players = Bid.objects.filter(amount__gt=0)
    sorted_sold_players = sorted(sold_players, key=lambda x: x.amount, reverse=True)

    
    top_10_sold_players = sorted_sold_players[:10]

    if search_query:
        sold_players = sold_players.filter(
            Q(player__name__icontains=search_query) |  
            Q(player__playertype__icontains=search_query) | 
            Q(amount__icontains=search_query) |
            Q(bidder__name__icontains=search_query)  
        )
    return render(request, 'sold_player.html', {'sold_players': sold_players,'top_10_sold_players': top_10_sold_players})


@login_required(login_url="/login/")
def team_details(request, team_name):
    team = Team.objects.get(name=team_name)
    bids = Bid.objects.filter(bidder=team)
    players = bids.select_related('player').all()
    
    # Calculate the total amount spent by the team
    total_spent = bids.aggregate(Sum('amount'))['amount__sum'] or 0

    # Calculate the remaining amount for the team
    team_amount = team.amount - total_spent 

    # Count players in different categories
    squad_count = players.count()
    batsmen_count = players.filter(player__playertype='Batsmen').count()
    bowler_count = players.filter(player__playertype='Bowler').count()
    allrounder_count = players.filter(player__playertype='Allrounder').count()

    return render(request, 'team_details.html', {'team': team, 'players': players, 'team_amount': team_amount ,'squad_count': squad_count,'batsmen_count': batsmen_count,'bowler_count': bowler_count,'allrounder_count': allrounder_count,})

def delete_player(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    player.delete()
    return redirect('all_players')

def delete_team(request, team_id):
    team = get_object_or_404(Team, id=team_id)
    team.delete()
    return redirect('all_teams')


def login_page(request):
    if request.method=="POST":
        username=request.POST.get('username')
        password=request.POST.get('password')

        if not User.objects.filter(username=username).exists():
            messages.error(request, "invalid usrrname")
            return redirect('/login/')
        
        user=authenticate(username=username,password=password)
        if user is None:
            messages.error(request, "invalid usrrname")
            return redirect('/login/')
        else:
            login(request,user)
            return redirect('/')

    return render(request,'login.html')

def logout_page(request):
    logout(request)
    return redirect('/login/')

def register(request):
    
    if request.method=="POST":
        first_name=request.POST.get('first_name')
        last_name=request.POST.get('last_name')
        username=request.POST.get('username')
        password=request.POST.get('password')
        image = request.FILES.get('image')

        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request, "Username already exists")
            return redirect('/register/')
        
        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
            image=image,
        )

        user.set_password(password)
        user.save()
        messages.info(request, "Account created succesfully")
        return redirect('/register/')
    
    return render(request,'register.html')


#---------------------------------------------------------------------------------------------------------------------

def select_teams(request):
    teams = Team.objects.all()

    if request.method == 'POST':
        batting_team_id = request.POST.get('batting_team')
        bowling_team_id = request.POST.get('bowling_team')

        batting_team = Team.objects.get(pk=batting_team_id)
        bowling_team = Team.objects.get(pk=bowling_team_id)

        # Create a new match
        match = Match.objects.create(batting_team=batting_team, bowling_team=bowling_team)

        # Redirect to the match preview page with the match ID
        return redirect('select_players_to_play', match_id=match.id)

    return render(request, 'selectteams.html', {'teams': teams})





def select_players_to_play(request, match_id):
    match = get_object_or_404(Match, id=match_id)

    batting_team_players = Bid.objects.filter(bidder=match.batting_team)
    bowling_team_players = Bid.objects.filter(bidder=match.bowling_team)

    return render(request, 'select_players_to_play.html', {
        'batting_team': match.batting_team,
        'bowling_team': match.bowling_team,
        'batting_team_players': batting_team_players,
        'bowling_team_players': bowling_team_players,
        'match_id': match_id,
    })


def match_preview(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    selected_player_ids = request.POST.getlist('selected_players')
    
    
    selected_players = Bid.objects.filter(id__in=selected_player_ids)
    batting_team_players = selected_players.filter(bidder=match.batting_team)
    bowling_team_players = selected_players.filter(bidder=match.bowling_team)

    return render(request, 'match_preview.html', {
        'match_id' : match_id,
        'batting_team': match.batting_team,
        'bowling_team': match.bowling_team,
        'selected_players': selected_players,
        'batting_team_players': batting_team_players,
        'bowling_team_players': bowling_team_players,
    })






from django.shortcuts import render

def initial_players(request):
    if request.method == 'POST':
        
        
        batting_team_players = request.POST.get('batting_team_players').split(',')
        bowling_team_players = request.POST.get('bowling_team_players').split(',')

        

        # Get the first two players as opening batsmen
        opening_batsmen = batting_team_players[:2]
        #opening_batsmen = batting_players_names[:2]
        # Get the first player as the opening bowler
        opening_bowler = bowling_team_players[0]
        batting_players_names = [bid.split('for')[-1].strip() for bid in batting_team_players]
        bowling_players_names=[bid.split('for')[-1].strip() for bid in bowling_team_players]
        return render(request, 'initialplayers.html', {
          #'batting_team_players': batting_team_players,
          'batting_team_players': batting_players_names,
          #'bowling_team_players': bowling_team_players,  
          'bowling_team_players':bowling_players_names,
           'opening_batsmen': opening_batsmen,
            'opening_bowler': opening_bowler,

        })

    return render(request, 'initialplayers.html')



    


#---------------------------------------------------------------------------------------------------------------------

#def player_detail(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    return render(request, 'player_detail.html', {'player': player})

def player_detail(request, player_id):
    try:
        player = get_object_or_404(Player, pk=player_id)
        return render(request, 'player_detail.html', {'player': player})
    except Exception as e:
        return render(request, 'showerror.html', {'error_message': str(e)}, status=500)
#---------------------------------------------------------------------------------------------

def x_selectteam(request):
    teams = Team.objects.all()
    if request.method == 'POST':
        batting_team_id = request.POST.get('batting_team')
        bowling_team_id = request.POST.get('bowling_team')

        batting_team = Team.objects.get(pk=batting_team_id)
        bowling_team = Team.objects.get(pk=bowling_team_id)
        

        # Create a new match
        match = Match.objects.create(batting_team=batting_team, bowling_team=bowling_team)

        # Redirect to the match preview page with the  ID
        return redirect('x_selectplayerstoplay', match_id=match.id, )
    return render(request,'x_selectteam.html', {'teams': teams})

def x_selectplayerstoplay(request,match_id):
    match = get_object_or_404(Match, id=match_id)

    batting_team_players = Bid.objects.filter(bidder=match.batting_team)
    bowling_team_players = Bid.objects.filter(bidder=match.bowling_team)
    batting_players = match.batting_team.players
    bowling_players = match.bowling_team.players


    return render(request, 'x_selectplayerstoplay.html', {
        'batting_team': match.batting_team,
        'bowling_team': match.bowling_team,
        'batting_team_players': batting_team_players,
        'bowling_team_players': bowling_team_players,
        'match_id': match_id,
        'batting_players':batting_players,
        'bowling_players':bowling_players,
    })


def x_matchpreview(request,match_id):
    match = get_object_or_404(Match, id=match_id)
    selected_player_ids = request.POST.getlist('selected_players')
    
    
    selected_players = Bid.objects.filter(id__in=selected_player_ids)
    batting_team_players = selected_players.filter(bidder=match.batting_team)
    bowling_team_players = selected_players.filter(bidder=match.bowling_team)

    

    return render(request, 'x_matchpreview.html', {
        'match_id' : match_id,
        'batting_team': match.batting_team,
        'bowling_team': match.bowling_team,
        'selected_players': selected_players,
        'batting_team_players': batting_team_players,
        'bowling_team_players': bowling_team_players,
    })

def y_a(request,match_id):
    match = get_object_or_404(Match, id=match_id)
    if request.method == 'POST':
        selected_player_ids = request.POST.getlist('selected_players')
        selected_players = Bid.objects.filter(id__in=selected_player_ids)
        batting_team_players = selected_players.filter(bidder=match.batting_team)
        bowling_team_players = selected_players.filter(bidder=match.bowling_team)

        return render(request, 'y_a.html', {
            'match_id': match_id,
            'batting_team': match.batting_team,
            'bowling_team': match.bowling_team,
            'selected_players': selected_players,
            'batting_team_players': batting_team_players,
            'bowling_team_players': bowling_team_players,
        })

    return render(request, 'y_a.html', {
       'match_id': match_id,
    })

#****************************************************************************

def add_venue(request):
    if request.method == 'POST':
        form = VenueForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('all_venues') 
    else:
        form = VenueForm()
    return render(request, 'add_venue.html', {'form': form})


def all_venues(request):
    venues = Venue.objects.all()
    return render(request, 'all_venues.html', {'venues': venues})

def all_venues(request):
    venues = Venue.objects.all()
    return render(request, 'all_venues.html', {'venues': venues})

def delete_venue(request, venue_id):
    venue = get_object_or_404(Venue, id=venue_id)
    venue.delete()
    return redirect('all_venues')

def all_of_teams(request):
    teams = Team.objects.all()
    #team_data = []

    #for team in teams:
        # Retrieve players auctioned for each team
        #players = Player.objects.filter(bid__bidder=team)
        #team_data.append({'team': team, 'players': players})

    #return render(request, 'all_of_teams.html', {'team_data': team_data})
    teams = Team.objects.all()

    return render(request, 'all_of_teams.html', {'teams': teams})

def all_of_team_details(request, team_id):
    team = get_object_or_404(Team, pk=team_id)
    
    players = Player.objects.filter(bid__bidder=team)
    return render(request, 'all_of_team_details.html', {'team': team, 'players': players})

def all_of_player_details(request, player_id):
    player = get_object_or_404(Player, pk=player_id)
    return render(request, 'all_of_player_details.html', {'player': player})

def top_10_runs(request):
    players = Player.objects.all()
    sorted_players = sorted(players, key=lambda x: x.runs_scored, reverse=True)
    

  
    top_10_players = sorted_players[:10]
    return render(request, 'top_10_runs.html', {'players': players,'top_10_players':top_10_players})


def top_10_buys(request):
    sold_players = Bid.objects.filter(amount__gt=0)
    sorted_sold_players = sorted(sold_players, key=lambda x: x.amount, reverse=True)

    
    top_10_sold_players = sorted_sold_players[:10]
    return render(request,'top_10_buys.html',{'sold_players':sold_players,'top_10_sold_players':top_10_sold_players})
############################################################################################


###################################################################

def add_score(request):
    players = Player.objects.all()
    return render(request,'add_score.html',{'players':players})

from django.http import JsonResponse
from .models import Player

def increase_runs(request, player_id):
    player = Player.objects.get(id=player_id)
    player.runs_scored += 1
    player.save()
    return JsonResponse({'success': True})

def decrease_runs(request, player_id):
    player = Player.objects.get(id=player_id)
    player.runs_scored -= 1
    player.save()
    return JsonResponse({'success': True})

def save_runs(request, player_id):
    try:
        player = Player.objects.get(id=player_id)
        
        player.runs_scored += 1  
        player.save()
        return JsonResponse({'success': True})
    except Player.DoesNotExist:
        return JsonResponse({'success': False, 'error': 'Player not found'})
    except Exception as e:
        return JsonResponse({'success': False, 'error': str(e)})
    
def increase_matches_played(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    player.matches_played += 1
    player.save()
    return JsonResponse({'success': True})

def decrease_matches_played(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    if player.matches_played > 0:
        player.matches_played -= 1
        player.save()
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'error': 'Matches played cannot be negative'})

def save_matches_played(request, player_id):
    player = get_object_or_404(Player, id=player_id)
    
    return JsonResponse({'success': True})

from .models import Post
from .forms import PostForm

def add_blog(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)  # Pass request.FILES to handle image upload
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'addblog.html', {'form': form})

def post_list(request):
    posts = Post.objects.all()
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm()
    return render(request, 'post_list.html', {'posts': posts, 'form': form})

def update_blog(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_list')
    else:
        form = PostForm(instance=post)
    return render(request, 'update_blog.html', {'form': form})

def delete_blog(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('post_list')
    return render(request, 'delete_blog.html', {'post': post})

def like_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.likes += 1
    post.save()
    return redirect('post_list')

def dislike_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.dislikes += 1
    post.save()
    return redirect('post_list')