# auction/forms.py
from django import forms
from .models import Team, Player

class CreateTeamForm(forms.ModelForm):
    class Meta:
        model = Team
        fields = ['name', 'amount', 'picture']

class AddPlayerForm(forms.ModelForm):
    class Meta:
        model = Player
        fields = ['name', 'playertype', 'base_price', 'picture']
