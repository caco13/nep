from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
import datetime


# Custom validators
# Valida data de nascimento:
# data de nascimento maior que a data atual
def validate_date_birth(value):
    if value > datetime.date.today():
        raise ValidationError(
            "Date of birth can't be greater than today date."
        )


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


class ProtocolComponent(models.Model):
    identification = models.CharField(max_length=50)
    description = models.TextField()
    duration_value = models.IntegerField(validators=[MinValueValidator(1)])
    duration_unit = models.CharField(max_length=15)
    component_type = models.CharField(max_length=30)
    experiment = models.ForeignKey(Experiment)


class Group(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    # TODO: to be done. ManyToMany
    # classification_of_diseases = models.ManyToManyField(
    # ClassificationOfDiseases)
    experiment = models.ForeignKey(Experiment)
    protocol_component = models.ForeignKey(
        ProtocolComponent, null=True, on_delete=models.SET_NULL
    )


class Gender(models.Model):
    name = models.CharField(max_length=50)


class MaritalStatus(models.Model):
    name = models.CharField(max_length=50)


class Participant(models.Model):
    date_birth = models.DateField(validators=[validate_date_birth])
    gender = models.ForeignKey(Gender)
    marital_status = models.ForeignKey(MaritalStatus)
    district = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    removed = models.BooleanField(default=False)
