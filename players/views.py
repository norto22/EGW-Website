from django.shortcuts import render
from .models import Player, Transaction

def main_page(request):
    players = Player.objects.all()
    transactions = Transaction.objects.all()
    players = Player.objects.all().order_by('discord_username')
    return render(request, 'main_page.html', {'players': players, 'transactions': transactions})


    
    

