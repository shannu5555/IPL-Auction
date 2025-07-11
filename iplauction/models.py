# auction/models.py
from django.db import models
from django.db.models import Sum
from datetime import date
import uuid





class Team(models.Model):
    name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='team_pics/', null=True, blank=True)

    def __str__(self):
        return self.name
    
    @property
    def players(self):
        # Retrieve the player names associated with the team's bids
        return [bid.player.name for bid in self.bid_set.all()]
    
    def squad_count(self):
        return self.bid_set.count()
    
    def total_amount_spent(self):
        bids = self.bid_set.filter(amount__gt=0)
        total_spent = bids.aggregate(Sum('amount'))['amount__sum'] or 0
        return float(self.amount - total_spent) 
    
    

class Player(models.Model):
    name=models.CharField(max_length=100)
    
    
    playertype = models.CharField(max_length=20, choices=[
        ('Batsmen', 'Batsmen'),
        ('Bowler', 'Bowler'),
        ('Allrounder', 'Allrounder'),
    ])
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    picture = models.ImageField(upload_to='player_pics/', null=True, blank=True)
    
    dob = models.DateField(null=True, blank=True)
    batting_style = models.CharField(max_length=100, choices=[
        ('Right-Handed-Bat', 'Right-Handed-Bat'),
        ('Left-Handed-Bat', 'Left-Handed-Bat'),
        
    ])
    runs_scored = models.IntegerField(default=0)
    wickets_taken = models.IntegerField(default=0)
    matches_played = models.IntegerField(default=0)
    
    international_team_name = models.CharField(max_length=100, blank=True)
    
    def __str__(self):
        return self.name
    
    def calculate_age(self):
        if self.dob:
            today = date.today()
            age = today.year - self.dob.year - ((today.month, today.day) < (self.dob.month, self.dob.day))
            return age
        return None
    def average_runs_per_match(self):
        if self.matches_played != 0:
            return round(self.runs_scored / self.matches_played, 2)
        else:
            return 0
    
    def save(self, *args, **kwargs):
        # Convert the name to uppercase before saving
        self.name = self.name.upper()
        super(Player, self).save(*args, **kwargs)

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

class Venue(models.Model):
    uuid = models.UUIDField(default=uuid.uuid4,unique=True, editable=False)
    venue_name = models.CharField(max_length=100)
    venue_location = models.CharField(max_length=100)
    capacity = models.PositiveIntegerField()
    venue_description = models.TextField()
    venue_picture = models.ImageField(upload_to='venue_pictures/')


class Post(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateField(auto_now_add=True)
    likes = models.IntegerField(default=0)
    dislikes = models.IntegerField(default=0)
    image = models.ImageField(upload_to='blog_images/', null=True, blank=True)

    def __str__(self):
        return self.title
