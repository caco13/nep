from rest_framework import serializers, generics, permissions

from experiments.models import Experiment, Study, User, Researcher, \
    TMSSetting, EEGSetting, EMGSetting, Manufacturer, Software, \
    SoftwareVersion, ProtocolComponent, Group, Gender, MaritalStatus, \
    Participant


# API Serializers
class ExperimentSerializer(serializers.ModelSerializer):
    study = serializers.ReadOnlyField(source='study.title')
    user = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Experiment
        fields = ('id', 'title', 'description', 'data_acquisition_done',
                  'study', 'user')


class UserSerializer(serializers.ModelSerializer):
    experiments = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Experiment.objects.all()
    )

    class Meta:
        model = User
        fields = ('id', 'username', 'experiments')


class StudySerializer(serializers.ModelSerializer):
    researcher = serializers.ReadOnlyField(source='researcher.first_name')
    experiments = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )

    class Meta:
        model = Study
        fields = ('id', 'title', 'description', 'start_date', 'end_date',
                  'researcher', 'experiments')


class ResearcherSerializer(serializers.ModelSerializer):
    studies = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )

    class Meta:
        model = Researcher
        fields = ('id', 'first_name', 'surname', 'email', 'studies')


class TMSSettingSerializer(serializers.ModelSerializer):
    experiment = serializers.ReadOnlyField(source='experiment.title')

    class Meta:
        model = TMSSetting
        fields = ('id', 'name', 'description', 'experiment')


class EEGSettingSerializer(serializers.ModelSerializer):
    experiment = serializers.ReadOnlyField(source='experiment.title')

    class Meta:
        model = EEGSetting
        fields = ('id', 'name', 'description', 'experiment')


class ManufacturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Manufacturer
        fields = ('id', 'name')


class SoftwareSerializer(serializers.ModelSerializer):
    manufacturer = serializers.ReadOnlyField(source='manufacturer.name')

    class Meta:
        model = Software
        fields = ('id', 'name', 'description', 'manufacturer')


class SoftwareVersionSerializer(serializers.ModelSerializer):
    software = serializers.ReadOnlyField(source='software.name')

    class Meta:
        model = SoftwareVersion
        fields = ('id', 'name', 'software')


class EMGSettingSerializer(serializers.ModelSerializer):
    software_version = serializers.ReadOnlyField(
        source='software_version.name')
    experiment = serializers.ReadOnlyField(source='experiment.title')

    class Meta:
        model = EMGSetting
        fields = ('id', 'name', 'description', 'software_version',
                  'experiment')


class ProtocolComponentSerializer(serializers.ModelSerializer):
    experiment = serializers.ReadOnlyField(source='experiment.title')

    class Meta:
        model = ProtocolComponent
        fields = ('id', 'identification', 'description', 'duration_value',
                  'duration_unit', 'component_type', 'experiment')


class GroupSerializer(serializers.ModelSerializer):
    experiment = serializers.ReadOnlyField(source='experiment.title')
    protocol_component = serializers.ReadOnlyField(
        source='protocol_experiment.title')

    class Meta:
        model = Group
        fields = ('id', 'title', 'description', 'experiment',
                  'protocol_component')


class GenderSerializer(serializers.ModelSerializer):

    class Meta:
        model = Gender
        fields = ('id', 'name')


class MaritalStatusSerializer(serializers.ModelSerializer):

    class Meta:
        model = MaritalStatus
        fields = ('id', 'name')


class ParticipantSerializer(serializers.ModelSerializer):
    group = serializers.ReadOnlyField(source='group.title')

    class Meta:
        model = Participant
        fields = ('id', 'date_birth', 'discrict', 'city', 'state',
                  'country', 'gender', 'marital_status', 'group')


# API Views
class ExperimentList(generics.ListCreateAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        study_id = self.kwargs.get('pk')
        study = Study.objects.filter(id=study_id).get()
        serializer.save(study=study, user=self.request.user)


class StudyList(generics.ListCreateAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        researcher_id = self.kwargs.get('pk')
        researcher = Researcher.objects.filter(id=researcher_id).get()
        serializer.save(researcher=researcher)


class ResearcherList(generics.ListCreateAPIView):
    queryset = Researcher.objects.all()
    serializer_class = ResearcherSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TMSSettingList(generics.ListCreateAPIView):
    queryset = TMSSetting.objects.all()
    serializer_class = TMSSettingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(experiment_id=self.kwargs.get('pk'))


class EEGSettingList(generics.ListCreateAPIView):
    queryset = EEGSetting.objects.all()
    serializer_class = EEGSettingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(experiment_id=self.kwargs.get('pk'))


class ManufacturerList(generics.ListCreateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class SoftwareList(generics.ListCreateAPIView):
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(manufacturer_id=self.kwargs.get('pk'))


class SoftwareVersionList(generics.ListCreateAPIView):
    queryset = SoftwareVersion.objects.all()
    serializer_class = SoftwareVersionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(software_id=self.kwargs.get('pk'))


class EMGSettingList(generics.ListCreateAPIView):
    queryset = EMGSetting.objects.all()
    serializer_class = EMGSettingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(software_version_id=self.kwargs.get('pk1'),
                        experiment_id=self.kwargs.get('pk2'))


class ProtocolComponentList(generics.ListCreateAPIView):
    queryset = ProtocolComponent.objects.all()
    serializer_class = ProtocolComponentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(experiment_id=self.kwargs.get('pk'))


class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(experiment_id=self.kwargs.get('pk1'),
                        experimental_protocol_id=self.kwargs.get('pk2'))


class GenderList(generics.ListAPIView):
    queryset = Gender.objects.all()
    serializer_class = GenderSerializer


class MaritalStatuslist(generics.ListAPIView):
    queryset = MaritalStatus.objects.all()
    serializer_class = MaritalStatusSerializer
