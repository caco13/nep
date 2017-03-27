from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator


class Researcher(models.Model):
    first_name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    email = models.EmailField(null=True)


class Study(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField(null=True)
    researcher = models.ForeignKey(Researcher, related_name='studies')


class Experiment(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    data_acquisition_done = models.BooleanField(default=False)
    study = models.ForeignKey(Study, related_name='experiments')
    user = models.ForeignKey(User)


class TMSSetting(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    experiment = models.ForeignKey(Experiment)


class EEGSetting(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    experiment = models.ForeignKey(Experiment)


class Manufacturer(models.Model):
    name = models.CharField(max_length=50)


class Software(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    manufacturer = models.ForeignKey(Manufacturer)


class SoftwareVersion(models.Model):
    name = models.CharField(max_length=150)
    software = models.ForeignKey(Software, related_name='versions')


class EMGSetting(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    software_version = models.ForeignKey(SoftwareVersion)
    experiment = models.ForeignKey(Experiment)


class Component(models.Model):
    identification = models.CharField(max_length=50)
    description = models.TextField()
    duration_value = models.IntegerField(validators=[MinValueValidator(1)])
    duration_unit = models.CharField(max_length=15)
    component_type = models.CharField(max_length=30)
    experiment = models.ForeignKey(Experiment)
