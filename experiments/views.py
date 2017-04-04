from django.shortcuts import render
from experiments.models import Experiment, Participant


def home_page(request):
    experiments = Experiment.objects.all()
    context = {'experiments_list': experiments}
    return render(request, 'experiments/home.html', context)


def participants_page(request):
    participants = Participant.objects.all()
    context = {'participants_list': participants}
    return render(request, 'experiments/participants.html', context)
