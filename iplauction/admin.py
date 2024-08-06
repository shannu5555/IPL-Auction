from django.contrib import admin

# Register your models here.
from .models import Player
from django.contrib import admin
from .models import Player
from .models import Team,Bid,Venue,Post
from django.contrib import admin




class PlayerAdmin(admin.ModelAdmin):
    pass

class TeamAdmin(admin.ModelAdmin):
    pass

class BidAdmin(admin.ModelAdmin):
    pass

class VenueAdmin(admin.ModelAdmin):
    pass

class PostAdmin(admin.ModelAdmin):
    pass

admin.site.register(Player, PlayerAdmin)
admin.site.register(Team, TeamAdmin)
admin.site.register(Bid,BidAdmin)
admin.site.register(Venue,VenueAdmin)
admin.site.register(Post,PostAdmin)

