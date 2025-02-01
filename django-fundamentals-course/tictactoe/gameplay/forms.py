from django.forms import ModelForm
from .models import Move
from django.core.exceptions import ValidationError

class MoveForm(ModelForm):
    class Meta:
        model = Move
        exclude = []

    def clean(self):
        x = self.cleaned_data.get("x")
        y = self.cleaned_data.get("y")
        game = self.instance.game
        if x is None or y is None:
            raise ValidationError("Coordinates are required")
        if game.board()[y][x] is not None:
            raise ValidationError("Square is not empty")
        return self.cleaned_data
