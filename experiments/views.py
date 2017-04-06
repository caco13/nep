from django.shortcuts import render
from reversion.models import Version
from django.contrib.auth.models import User

from experiments.models import Experiment, Participant, Study


# Table with experiments
def home_page(request):
    experiments = Experiment.objects.all()
    context = {'experiments_list': experiments}
    return render(request, 'experiments/home.html', context)


def experiment_detail(request, experiment_id):
    experiment = Experiment.objects.filter(id=experiment_id).get()
    versions = Version.objects.get_for_object(experiment)
    number_of_versions = len(versions) - 1
    context = {'experiment': experiment, 'versions': number_of_versions}
    return render(request, 'experiments/detail.html', context)


def experiment_versions(request, experiment_id):
    experiment = Experiment.objects.filter(id=experiment_id).get()
    versions = Version.objects.get_for_object(experiment)

    # make a list of version dictionaries to facilitates rendering in template
    # TODO: make a private method?
    # TODO: is that the best way?
    versions_list = list()
    versions_length = len(versions)
    for i in range(0, versions_length - 1):
        study = Study.objects.filter(id=versions[i].field_dict[
            'study_id']).get()
        owner = User.objects.filter(id=versions[i].field_dict[
            'owner_id']).get()
        versions_list.append({
            'title': versions[i].field_dict['title'],
            'description': versions[i].field_dict['description'],
            'study': study.title,
            'owner': owner.username,
            'date': versions[i].revision.date_created,
            'version': versions_length - 1 - i
        })

    context = {'versions': versions_list}
    return render(request, 'experiments/versions.html', context)


def participants_page(request):
    participants = Participant.objects.all()
    context = {'participants_list': participants}
    return render(request, 'experiments/participants.html', context)
