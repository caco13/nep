from django.db import models
from django.contrib.auth.models import User
from reversion.models import Revision
import reversion


class Researcher(models.Model):
    first_name = models.CharField(max_length=150, blank=True)
    surname = models.CharField(max_length=150, blank=True)
    email = models.EmailField(blank=True)
    nes_id = models.PositiveIntegerField()
    owner = models.ForeignKey(User)

    class Meta:
        unique_together = ('nes_id', 'owner')


class Study(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    nes_id = models.PositiveIntegerField()
    researcher = models.ForeignKey(Researcher, related_name='studies',
                                   default=None)
    owner = models.ForeignKey(User)

    class Meta:
        unique_together = ('nes_id', 'owner')


class ExperimentStatus(models.Model):
    tag = models.CharField(max_length=20)
    name = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)


@reversion.register()
class Experiment(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    data_acquisition_done = models.BooleanField(default=False)
    ethics_committee_file = models.FileField(
        'Project file approved by the ethics committee', blank=True
    )
    version = models.PositiveIntegerField()
    study = models.ForeignKey(Study, related_name='experiments')
    status = models.ForeignKey(ExperimentStatus, related_name='experiments',
                               default=1)  # TODO: requires 'to_be_approved'
    # has id 1.
    nes_id = models.PositiveIntegerField()
    owner = models.ForeignKey(User)

    class Meta:
        unique_together = ('nes_id', 'owner', 'version')


@reversion.register()
class ProtocolComponent(models.Model):
    identification = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    duration_value = models.IntegerField(null=True)
    component_type = models.CharField(max_length=30)
    nes_id = models.PositiveIntegerField()
    experiment = models.ForeignKey(Experiment,
                                   related_name='protocol_components')
    owner = models.ForeignKey(User)

    class Meta:
        unique_together = ('nes_id', 'owner', 'experiment')


class Group(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    protocol_component = models.ForeignKey(
        ProtocolComponent, null=True, blank=True)
    experiment = models.ForeignKey(Experiment, related_name='groups')
    nes_id = models.PositiveIntegerField()
    owner = models.ForeignKey(User)

    class Meta:
        unique_together = ('nes_id', 'owner', 'experiment')
