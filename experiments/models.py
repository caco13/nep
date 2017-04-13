from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
import datetime
import reversion


# Custom validators

# Valida data:
# data não pode ser maior que a atual
def validate_future_date(value):
    if value > datetime.date.today():
        raise ValidationError(
            "This date cannot be greater than today date."
        )


class Researcher(models.Model):
    # We are using blank=True to permit POST with blank fields
    # from User model in nes.
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
    start_date = models.DateField(validators=[validate_future_date])
    # TODO: See if null=True or blank=True. Last gave error.
    end_date = models.DateField(null=True)
    # TODO: add keywords (see ResearchProject nes experiment model)
    nes_id = models.PositiveIntegerField()
    researcher = models.ForeignKey(Researcher, related_name='studies')
    owner = models.ForeignKey(User)
    reversion.register(Researcher, follow=['studies'])

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('nes_id', 'owner')


class ExperimentStatus(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

    def __str__(self):
        return self.name


# TODO: is there a best solution? See Experiment.
# TODO: http://stackoverflow.com/questions/9311996/setting-default-value-for
# TODO: -foreign-key-attribute#9312738
DEFAULT_STATUS = 1


@reversion.register()
class Experiment(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField()
    data_acquisition_done = models.BooleanField(default=False)
    study = models.ForeignKey(Study, related_name='experiments')
    nes_id = models.PositiveIntegerField()
    owner = models.ForeignKey(User)
    status = models.ForeignKey(ExperimentStatus, default=DEFAULT_STATUS)
    reversion.register(Study, follow=['experiments'])

    def __str__(self):
        return self.title

    class Meta:
        unique_together = ('nes_id', 'owner')


class ProtocolComponent(models.Model):
    identification = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    duration_value = models.IntegerField(null=True)
    duration_unit = models.CharField(max_length=15, blank=True)
    component_type = models.CharField(max_length=30)
    nes_id = models.PositiveIntegerField()
    experiment = models.ForeignKey(Experiment)
    owner = models.ForeignKey(User)

    class Meta:
        unique_together = ('nes_id', 'owner')


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


class Group(models.Model):
    title = models.CharField(max_length=50)
    description = models.TextField(blank=True)
    # TODO: to be done. ManyToMany
    # classification_of_diseases = models.ManyToManyField(
    # ClassificationOfDiseases)
    nes_id = models.PositiveIntegerField()
    protocol_component = models.ForeignKey(
        ProtocolComponent, null=True, on_delete=models.SET_NULL
    )
    owner = models.ForeignKey(User)

    class Meta:
        unique_together = ('nes_id', 'owner')


class Participant(models.Model):
    date_birth = models.DateField(validators=[validate_future_date])
    district = models.CharField(max_length=50, blank=True)
    city = models.CharField(max_length=30, blank=True)
    state = models.CharField(max_length=30, blank=True)
    country = models.CharField(max_length=30, blank=True)
    gender = models.CharField(max_length=20)
    marital_status = models.CharField(max_length=30, blank=True)
    nes_id = models.PositiveIntegerField()
    groups = models.ManyToManyField(Group)
    owner = models.ForeignKey('auth.User', related_name='participants')

    class Meta:
        unique_together = ('nes_id', 'owner')


class ExamFile(models.Model):
    # exam = models.ForeignKey(ComplementaryExam, null=False)
    content = models.FileField()
    owner = models.ForeignKey('auth.User')
