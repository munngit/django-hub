from django.shortcuts import render, redirect


def welcome(request):
    if request.user.is_authenticated:
        return redirect('player_home') #name of page we want to redirect to. so make sure to give name to page in url.py
    else:

        return render(request,"tictactoe/welcome.html")



# Create your views here.
