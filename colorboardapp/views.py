from django.shortcuts import render
# Create your views here.
from django.views.generic.edit import FormView

from colorboardapp.forms import GameForm


class GameView(FormView):
    template_name = 'home.html'
    form_class = GameForm

    def form_valid(self, form):
        instance = None
        if form.is_valid():
            instance = form.save()
        return render(self.request, 'home.html', self.get_context_data(instance=instance))
