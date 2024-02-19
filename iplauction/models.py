# auction/models.py
from django.db import models
from django.db.models import Sum


class Team(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='team_pics/', null=True, blank=True)

    def __str__(self):
        return self.name
    
    def total_amount_spent(self):
        bids = self.bid_set.filter(amount__gt=0)
        total_spent = bids.aggregate(Sum('amount'))['amount__sum'] or 0
        return self.amount - total_spent

class Player(models.Model):
    name = models.CharField(max_length=100)
    playertype = models.CharField(max_length=20, choices=[
        ('Batsmen', 'Batsmen'),
        ('Bowler', 'Bowler'),
        ('Allrounder', 'Allrounder'),
    ])
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='player_pics/', null=True, blank=True)

    def __str__(self):
        return self.name

class Bid(models.Model):
    player = models.ForeignKey(Player, on_delete=models.CASCADE)
    bidder = models.ForeignKey(Team, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.bidder.name} bids {self.amount} for {self.player.name}"

# auction/models.py

# auction/models.py
class Match(models.Model):
    batting_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='batting_team')
    bowling_team = models.ForeignKey(Team, on_delete=models.CASCADE, related_name='bowling_team')
    team_score = models.IntegerField(default=0)
    overs = models.FloatField(default=0)

    def __str__(self):
        return f"Match between {self.batting_team.name} and {self.bowling_team.name}"

