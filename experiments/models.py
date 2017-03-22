from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Researcher(models.Model):
    first_name = models.CharField(max_length=150, default='')
    surname = models.CharField(max_length=150, default='')
    email = models.EmailField(null=True)


class Study(models.Model):
    title = models.CharField(max_length=150, default='')
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    researcher = models.ForeignKey(Researcher, related_name='studies',
                                   default='')


class Experiment(models.Model):
    title = models.CharField(max_length=150, default='')
    description = models.TextField(default='')
    data_acquisition_done = models.BooleanField(default=False)
    study = models.ForeignKey(Study, related_name='experiments')
    owner = models.ForeignKey(User, default='')


class TMSSetting(models.Model):
    name = models.CharField(max_length=150, default='')
    description = models.TextField(default='')
    experiment = models.ForeignKey(Experiment, default='')


class EEGSetting(models.Model):
    name = models.CharField(max_length=150, default='')
    description = models.TextField(default='')
    experiment = models.ForeignKey(Experiment, default='')


class Manufacturer(models.Model):
    name = models.CharField(max_length=50, default='')


class Software(models.Model):
    name = models.CharField(max_length=150, default='')
    description = models.TextField(default='')
    manufacturer = models.ForeignKey(Manufacturer, default='')


class SoftwareVersion(models.Model):
    name = models.CharField(max_length=150, default='')
    software = models.ForeignKey(Software, related_name='versions')


class EMGSetting(models.Model):
    name = models.CharField(max_length=150, default='')
    description = models.TextField(default='')
    software_version = models.ForeignKey(SoftwareVersion, default='')
    experiment = models.ForeignKey(Experiment, default='')


class Component(models.Model):
    identification = models.CharField(max_length=50, default='')
    description = models.TextField(default='')
    duration_value = models.IntegerField(default='', validators=[
        MinValueValidator(1)])
    duration_unit = models.CharField(max_length=15, default='')
    component_type = models.CharField(max_length=30, default='')
    experiment = models.ForeignKey(Experiment, default='')
