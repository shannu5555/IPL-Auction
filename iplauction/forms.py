# auction/forms.py
from django import forms
from .models import Team, Player,Venue
from .models import Post

class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'amount', 'picture']

class AddPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name',  'playertype', 'base_price', 'picture','dob','batting_style','international_team_name',]

class VenueForm(forms.ModelForm):
    class Meta:
        model = Venue
        fields = ['venue_name', 'venue_location', 'capacity', 'venue_description', 'venue_picture']

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'description', 'likes', 'image']