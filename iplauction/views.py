# auction/views.py
from django.shortcuts import render, redirect
from .models import Team, Player, Bid ,Match
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


@login_required(login_url="/login/")
def home(request):
    return render(request, 'home.html')

def x(request):
    return render(request, 'x.html')

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
    return render(request, 'team_details.html', {'team': team, 'players': players, 'team_amount': team_amount})

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
    return render(request, 'all_player.html', {'players': players})


@login_required(login_url="/login/")
def auction_page(request):
    players = Player.objects.filter(bid__isnull=True)
    live_bidding_amount = get_live_bidding_amount()
    last_bids = get_last_bids()

    team_amounts = Team.objects.annotate(total_amount_spent=Sum('bid__amount'))

    # Ensure you're passing the necessary context data
    return render(request, 'auction.html', {
        'players': players,
        'live_bidding_amount': live_bidding_amount,
        'last_bids': last_bids,
        'teams': Team.objects.all(),  # Include teams for bidder selection
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
    # Implement logic to get the last bid details
    # This could be the last bid for each player in the auction
    return Bid.objects.filter(amount__gt=0).order_by('-id')[:5]  # Assuming you want the last 5 bids

@login_required(login_url="/login/")
def sold_players(request):
    search_query = request.GET.get('search', '')
    sold_players = Bid.objects.filter(amount__gt=0)

    if search_query:
        sold_players = sold_players.filter(
            Q(player__name__startswith=search_query) |  # Search by player name Q(player__name__icontains=search_query) |
            Q(player__playertype__startswith=search_query) |  # Search by player type
            Q(amount__startswith=search_query) |  # Search by amount
            Q(bidder__name__startswith=search_query)  # Search by bidder name
        )
    return render(request, 'sold_player.html', {'sold_players': sold_players})


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
            return redirect('/homi/')

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
         
        user=User.objects.filter(username=username)
        if user.exists():
            messages.info(request, "Username already exists")
            return redirect('/register/')

        user=User.objects.create(
            first_name=first_name,
            last_name=last_name,
            username=username,
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
        'batting_team': match.batting_team,
        'bowling_team': match.bowling_team,
        'selected_players': selected_players,
        'batting_team_players': batting_team_players,
        'bowling_team_players': bowling_team_players,
        'match_id': 12,
    })

def match_preview(request, match_id):
    match = get_object_or_404(Match, id=match_id)
    selected_player_ids = request.POST.getlist('selected_players')

    selected_players = Bid.objects.filter(id__in=selected_player_ids)
    batting_team_players = selected_players.filter(bidder=match.batting_team)
    bowling_team_players = selected_players.filter(bidder=match.bowling_team)

    return render(request, 'match_preview.html', {
        'batting_team': match.batting_team,
        'bowling_team': match.bowling_team,
        'selected_players': selected_players,
        'batting_team_players': batting_team_players,
        'bowling_team_players': bowling_team_players,
    })

def initial_players(request):
    
    if request.method == 'POST':
        
        
        batting_team_players = request.POST.get('batting_team_players').split(',')
        bowling_team_players = request.POST.get('bowling_team_players').split(',')

        # Get the first two players as opening batsmen
        opening_batsmen = batting_team_players[:2]

        # Get the first player as the opening bowler
        opening_bowler = bowling_team_players[0]

        return render(request, 'initialplayers.html', {
            'batting_team_players': batting_team_players,
            'bowling_team_players': bowling_team_players,
            'opening_batsmen': opening_batsmen,
            'opening_bowler': opening_bowler,
            
        })

    return render(request, 'initialplayers.html')




def initial_players(request):
    if request.method == 'POST':
        
        
        batting_team_players = request.POST.get('batting_team_players').split(',')
        bowling_team_players = request.POST.get('bowling_team_players').split(',')

        # Get the first two players as opening batsmen
        opening_batsmen = batting_team_players[:2]

        # Get the first player as the opening bowler
        opening_bowler = bowling_team_players[0]

        return render(request, 'initialplayers.html', {
            'batting_team_players': batting_team_players,
            'bowling_team_players': bowling_team_players,
            'opening_batsmen': opening_batsmen,
            'opening_bowler': opening_bowler,
        })

    return render(request, 'initialplayers.html')


    


#---------------------------------------------------------------------------------------------------------------------



