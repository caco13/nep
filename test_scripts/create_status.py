from experiments.models import ExperimentStatus

ExperimentStatus.objects.create(
    name='to_be_approved',
    description='To be Approved'
)
ExperimentStatus.objects.create(
    name='approved',
    description='Approved'
)
ExperimentStatus.objects.create(
    name='rejected',
    description='Rejected'
)
