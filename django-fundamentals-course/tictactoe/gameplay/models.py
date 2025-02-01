from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth.models import User
from django.db.models import Q
from django.urls import reverse

# Game Status Choices
GAME_STATUS_CHOICES = (
    ('F', 'First Player To Move'),
    ('S', 'Second Player To Move'),
    ('W', 'First Player Wins'),
    ('L', 'Second Player Wins'),
    ('D', 'Draw')
)

BOARD_SIZE = 3  # Tic-Tac-Toe board size


class GamesQuerySet(models.QuerySet):
    def games_for_user(self, user):
        return self.filter(
            Q(first_player=user) | Q(second_player=user)
        ).distinct()

    def active(self):
        return self.filter(
            Q(status='F') | Q(status='S')
        )


class Game(models.Model):
    first_player = models.ForeignKey(User, related_name="games_first_player", on_delete=models.CASCADE)
    second_player = models.ForeignKey(User, related_name="games_second_player", on_delete=models.CASCADE)

    start_time = models.DateTimeField(auto_now_add=True)
    last_active = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, default='F', choices=GAME_STATUS_CHOICES)

    objects = GamesQuerySet.as_manager()

    def board(self):
        """Return a 2D list representing the game board."""
        board = [[None for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        for move in self.move_set.all():
            board[move.y][move.x] = move
        return board

    def is_users_move(self, user):
        return (
            (user == self.first_player and self.status == 'F') or
            (user == self.second_player and self.status == 'S')
        )

    def new_move(self):
        """Creates a new move for the current player."""
        if self.status not in ['F', 'S']:
            raise ValueError("Cannot make a move on a finished game")

        return Move(
            game=self,
            by_first_player=self.status == 'F'
        )

    def update_after_move(self, move):
        """Updates the game state after a move is made."""
        self.status = self._get_game_status_after_move(move)
        self.save()

    def _get_game_status_after_move(self, move):
        """Determines the new game status after a move."""
        x, y = move.x, move.y
        board = self.board()

        def is_winning_line(a, b, c):
            return a is not None and a == b == c  # Ensures all are filled and match

        # Check Rows, Columns, and Diagonals for a Win
        if is_winning_line(board[y][0], board[y][1], board[y][2]) or \
           is_winning_line(board[0][x], board[1][x], board[2][x]) or \
           is_winning_line(board[0][0], board[1][1], board[2][2]) or \
           is_winning_line(board[2][0], board[1][1], board[0][2]):
            return "W" if move.by_first_player else "L"

        # Check if Board is Full (Draw)
        if all(cell is not None for row in board for cell in row):
            return "D"

        # Otherwise, switch turns
        return "S" if self.status == "F" else "F"

    def get_absolute_url(self):
        return reverse('gameplay_detail', args=[self.id])

    def __str__(self):
        return f"{self.first_player} vs {self.second_player}"


class Move(models.Model):
    x = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(BOARD_SIZE - 1)]
    )
    y = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(BOARD_SIZE - 1)]
    )
    comment = models.CharField(max_length=300, blank=True)
    by_first_player = models.BooleanField(editable=False)
    game = models.ForeignKey(Game, related_name="move_set", on_delete=models.CASCADE, editable=False)

    def __eq__(self, other):
        """Compares moves based on player and position."""
        if not isinstance(other, Move):
            return False
        return (
            self.by_first_player == other.by_first_player and
            self.x == other.x and
            self.y == other.y
        )

    def __hash__(self):
        """Fixes unhashable type error by defining a unique hash based on primary key."""
        return hash(self.id)

    def save(self, *args, **kwargs):
        """Saves the move and updates the game status properly."""
        super(Move, self).save(*args, **kwargs)
        self.game.update_after_move(self)
        self.game.save()  # Ensure the game status is updated in the database

    def __str__(self):
        """Returns a readable representation of the move."""
        return f"Move by {'First' if self.by_first_player else 'Second'} Player at ({self.x}, {self.y})"
