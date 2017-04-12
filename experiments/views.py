from django.shortcuts import render
from reversion.models import Version
from django.contrib.auth.models import User

from experiments.models import Experiment, Participant, Study


# Table with experiments
def home_page(request):
    experiments = Experiment.objects.all()
    context = {'experiments_list': experiments}
    return render(request, 'experiments/index.html', context)


def experiment_detail(request, experiment_id):
    experiment = Experiment.objects.filter(id=experiment_id).get()
    versions = Version.objects.get_for_object(experiment)
    number_of_versions = len(versions)
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
    for i in range(0, versions_length):
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
            'version': versions_length - i
        })

    context = {'versions': versions_list, 'experiment_id': experiment_id}
    return render(request, 'experiments/versions.html', context)


def experiment_version_detail(request, experiment_id, version):
    experiment = Experiment.objects.filter(id=experiment_id).get()
    versions = Version.objects.get_for_object(experiment)
    versions_length = len(versions)
    version = int(version)
    study = Study.objects.filter(id=versions[versions_length -
                                             version].field_dict[
        'study_id']).get()
    owner = User.objects.filter(id=versions[versions_length -
                                            version].field_dict[
        'owner_id']).get()

    experiment_version = {
        'title': versions[versions_length - version].field_dict['title'],
        'description': versions[versions_length - version].field_dict[
            'description'],
        'study': study.title,
        'owner': owner.username,
        'date': versions[versions_length - version].revision.date_created,
        'version': version
    }

    context = {'experiment_version': experiment_version}
    return render(request, 'experiments/version_detail.html', context)


def participants_page(request):
    participants = Participant.objects.all()
    context = {'participants_list': participants}
    return render(request, 'experiments/participants.html', context)


def experiment_study(request, experiment_id):
    experiment = Experiment.objects.filter(id=experiment_id).get()
    study = experiment.study
    context = {'study': study}
    return render(request, 'experiments/study_detail.html', context)
