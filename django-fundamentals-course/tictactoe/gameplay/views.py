from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.views.generic import ListView

from .models import Game
from .forms import MoveForm

@login_required
def game_detail(request, id):
    """Display the details of a specific game."""
    game = get_object_or_404(Game, pk=id)
    context = {'game': game, 'board': game.board()}
    if game.is_users_move(request.user):
        context['form'] = MoveForm()
    return render(request, "gameplay/game_detail.html", context)

@login_required
def make_move(request, id):
    """Handle a move in the game."""
    game = get_object_or_404(Game, pk=id)
    if not game.is_users_move(request.user):
        raise PermissionDenied

    move = game.new_move()
    form = MoveForm(instance=move, data=request.POST)

    if form.is_valid():
        move.save()
        return redirect("game_detail", id=id)


    else:
        return render(request, "gameplay/game_detail.html", {'game': game, 'form': form})

class AllGamesList(ListView):
    """Display a list of all games."""
    model = Game
    template_name = "gameplay/all_games.html"
    context_object_name = "games"
