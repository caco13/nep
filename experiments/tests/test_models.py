from django.test import TestCase
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from experiments.models import Experiment, Study, Researcher
from datetime import datetime


class ExperimentModelTest(TestCase):

    def test_default_attributes(self):
        experiment = Experiment()
        self.assertEqual(experiment.title, '')
        self.assertEqual(experiment.description, '')
        self.assertEqual(experiment.data_acquisition_done, False)

    def test_cannot_save_empty_attributes(self):
        user = User.objects.create()
        study = Study.objects.create(start_date=datetime.utcnow())
        experiment = Experiment(
            title='', description='', study=study, user=user
        )
        with self.assertRaises(ValidationError):
            experiment.save()
            experiment.full_clean()

    def test_experiment_is_related_to_study_and_user(self):
        user = User.objects.create()
        study = Study.objects.create(start_date=datetime.utcnow())
        experiment = Experiment()
        experiment.user = user
        experiment.study = study
        experiment.save()
        self.assertIn(experiment, study.experiment_set.all())


class StudyModelTest(TestCase):

    def test_default_attributes(self):
        study = Study()
        self.assertEqual(study.title, '')
        self.assertEqual(study.description, '')
        self.assertEqual(study.start_date, None)
        self.assertEqual(study.end_date, None)

    def test_cannot_save_empty_attributes(self):
        # TODO: is it necessary to test for one attribute at time too?
        study = Study(title='', description='', start_date='')
        with self.assertRaises(ValidationError):
            study.save()
            study.full_clean()


class ResearcherModelTest(TestCase):

    def test_default_attributes(self):
        researcher = Researcher()
        self.assertEqual(researcher.first_name, '')
        self.assertEqual(researcher.surname, '')
        self.assertEqual(researcher.email, None)
