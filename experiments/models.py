from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator
from django.core.exceptions import ValidationError
import datetime


# Custom validators

# Valida data:
# data não pode ser maior que a atual
def validate_future_date(value):
    if value > datetime.date.today():
        raise ValidationError(
            "This date cannot be greater than today date."
        )


class Researcher(models.Model):
    first_name = models.CharField(max_length=150)
    surname = models.CharField(max_length=150)
    email = models.EmailField(null=True)
    nes_id = models.PositiveIntegerField()
    owner = models.ForeignKey(User)

    class Meta:
        unique_together = ('nes_id', 'owner')


class Study(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    start_date = models.DateField(validators=[validate_future_date])
    end_date = models.DateField(null=True)
    nes_id = models.PositiveIntegerField()
    researcher = models.ForeignKey(Researcher, related_name='studies')
    owner = models.ForeignKey(User)

    class Meta:
        unique_together = ('nes_id', 'owner')


class Experiment(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    data_acquisition_done = models.BooleanField(default=False)
    study = models.ForeignKey(Study, related_name='experiments')
    nes_id = models.PositiveIntegerField()
    owner = models.ForeignKey(User)


class TMSSetting(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    nes_id = models.PositiveIntegerField()
    experiment = models.ForeignKey(Experiment)
    owner = models.ForeignKey(User)


class EEGSetting(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    nes_id = models.PositiveIntegerField()
    experiment = models.ForeignKey(Experiment)
    owner = models.ForeignKey(User)


class Manufacturer(models.Model):
    name = models.CharField(max_length=50)
    nes_id = models.PositiveIntegerField()
    owner = models.ForeignKey(User)


class Software(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    nes_id = models.PositiveIntegerField()
    manufacturer = models.ForeignKey(Manufacturer)
    owner = models.ForeignKey(User)


class SoftwareVersion(models.Model):
    name = models.CharField(max_length=150)
    nes_id = models.PositiveIntegerField()
    software = models.ForeignKey(Software, related_name='versions')
    owner = models.ForeignKey(User)


class EMGSetting(models.Model):
    name = models.CharField(max_length=150)
    description = models.TextField()
    software_version = models.ForeignKey(SoftwareVersion)
    nes_id = models.PositiveIntegerField()
    experiment = models.ForeignKey(Experiment)
    owner = models.ForeignKey(User)


class ProtocolComponent(models.Model):
    identification = models.CharField(max_length=50)
    description = models.TextField()
    duration_value = models.IntegerField(validators=[MinValueValidator(1)])
    duration_unit = models.CharField(max_length=15)
    component_type = models.CharField(max_length=30)
    nes_id = models.PositiveIntegerField()
    experiment = models.ForeignKey(Experiment)
    owner = models.ForeignKey(User)


class Group(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField()
    # TODO: to be done. ManyToMany
    # classification_of_diseases = models.ManyToManyField(
    # ClassificationOfDiseases)
    nes_id = models.PositiveIntegerField()
    experiment = models.ForeignKey(Experiment)
    protocol_component = models.ForeignKey(
        ProtocolComponent, null=True, on_delete=models.SET_NULL
    )
    owner = models.ForeignKey(User)


class Participant(models.Model):
    date_birth = models.DateField(validators=[validate_future_date])
    district = models.CharField(max_length=50)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    gender = models.CharField(max_length=20)
    marital_status = models.CharField(max_length=30)
    nes_id = models.PositiveIntegerField()
    group = models.ForeignKey(Group)
    owner = models.ForeignKey('auth.User', related_name='participants')
