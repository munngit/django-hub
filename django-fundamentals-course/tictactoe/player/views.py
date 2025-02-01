from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy

from .forms import InvitationForm
from .models import Invitation
from gameplay.models import Game


@login_required
def home(request):
    """Render the home page with active and finished games, and invitations."""
    my_games = Game.objects.games_for_user(request.user)

    finished_games = my_games.filter(status__in=['W', 'L', 'D'])  # ✅ Only completed games
    active_games = my_games.filter(status__in=['F', 'S', 'P'])  # ✅ Includes pending games

    invitations = request.user.invitations_received.all()  # ✅ Define invitations

    return render(request, "player/home.html", {
        'active_games': active_games,
        'finished_games': finished_games,
        'invitations': invitations
    })

@login_required
def new_invitation(request):
    """Handle the creation of a new invitation."""
    if request.method == 'POST':
        invitation = Invitation(from_user=request.user)
        form = InvitationForm(instance=invitation, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('player_home')
    else:
        form = InvitationForm()
    return render(request, "player/new_invitation_form.html", {'form': form})


@login_required
def accept_invitation(request, id):
    """Handle accepting an invitation."""
    invitation = get_object_or_404(Invitation, pk=id)
    if not request.user == invitation.to_user:
        raise PermissionDenied
    if request.method == 'POST':
        if "accept" in request.POST:
            game = Game.objects.create(
                first_player=invitation.to_user,
                second_player=invitation.from_user,
            )
            invitation.delete()
            return redirect("game_detail", id=game.id)

    else:
        return render(request, "player/accept_invitation_form.html", {'invitation': invitation})


class SignUpView(CreateView):
    """Allow users to sign up."""
    form_class = UserCreationForm
    template_name = "player/signup_form.html"
    success_url = reverse_lazy('player_home')
