from rest_framework import serializers, generics, permissions
from rest_framework import parsers

from experiments.models import Experiment, Study, User, Researcher, \
    TMSSetting, EEGSetting, EMGSetting, Manufacturer, Software, \
    SoftwareVersion, ProtocolComponent, Group, Participant, ExamFile


# API Serializers
class ExperimentSerializer(serializers.ModelSerializer):
    study = serializers.ReadOnlyField(source='study.title')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Experiment
        fields = ('id', 'title', 'description', 'data_acquisition_done',
                  'nes_id', 'study', 'owner')


class OwnerSerializer(serializers.ModelSerializer):
    experiments = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Experiment.objects.all()
    )
    participants = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Participant.objects.all())

    class Meta:
        model = User
        fields = ('id', 'username', 'experiments', 'participants')


class StudySerializer(serializers.ModelSerializer):
    researcher = serializers.ReadOnlyField(source='researcher.first_name')
    experiments = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )

    class Meta:
        model = Study
        fields = ('id', 'title', 'description', 'start_date', 'end_date',
                  'nes_id', 'researcher', 'experiments')


class ResearcherSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')
    studies = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )

    class Meta:
        model = Researcher
        fields = ('id', 'first_name', 'surname', 'email', 'nes_id',
                  'studies', 'owner')


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
                  'duration_unit', 'component_type', 'nes_id', 'experiment')


class GroupSerializer(serializers.ModelSerializer):
    # TODO: owner missing
    protocol_component = serializers.ReadOnlyField(
        source='protocol_component.identification')

    class Meta:
        model = Group
        fields = ('id', 'title', 'description', 'nes_id', 'protocol_component')


class ParticipantSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='auth.user.username')

    class Meta:
        model = Participant
        fields = ('id', 'date_birth', 'district', 'city', 'state',
                  'country', 'gender', 'marital_status', 'nes_id', 'owner')


class ExamFileSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = ExamFile
        fields = ('content', 'owner')


# API Views
class ExperimentList(generics.ListCreateAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        study = Study.objects.filter(
            nes_id=self.kwargs.get('pk'), owner=self.request.user.id
        ).get()
        serializer.save(study=study, owner=self.request.user)


class StudyList(generics.ListCreateAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        researcher = Researcher.objects.filter(
            nes_id=self.kwargs.get('pk'), owner=self.request.user.id
        ).get()
        serializer.save(researcher=researcher, owner=self.request.user)


class ResearcherList(generics.ListCreateAPIView):
    queryset = Researcher.objects.all()
    serializer_class = ResearcherSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class TMSSettingList(generics.ListCreateAPIView):
    queryset = TMSSetting.objects.all()
    serializer_class = TMSSettingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        experiment = Experiment.objects.filter(
            nes_id=self.kwargs.get('pk'), owner=self.request.user
        ).get()
        serializer.save(experiment=experiment, owner=self.request.user)


class EEGSettingList(generics.ListCreateAPIView):
    queryset = EEGSetting.objects.all()
    serializer_class = EEGSettingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        experiment = Experiment.objects.filter(
            nes_id=self.kwargs.get('pk'), owner=self.request.user
        ).get()
        serializer.save(experiment=experiment)


class ManufacturerList(generics.ListCreateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class SoftwareList(generics.ListCreateAPIView):
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        manufacturer = Manufacturer.objects.filter(
            nes_id=self.kwargs.get('pk'), owner=self.request.user
        ).get
        serializer.save(manufacturer=manufacturer, owner=self.request.user)


class SoftwareVersionList(generics.ListCreateAPIView):
    queryset = SoftwareVersion.objects.all()
    serializer_class = SoftwareVersionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        software = Software.objects.filter(
            nes_id=self.kwargs.get('pk'), owner=self.request.user
        ).get()
        serializer.save(software=software, owner=self.request.user)


class EMGSettingList(generics.ListCreateAPIView):
    queryset = EMGSetting.objects.all()
    serializer_class = EMGSettingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        software_version = SoftwareVersion.objects.filter(
            nes_id=self.kwargs.get('pk1'), owner=self.request.user
        ).get()
        experiment = Experiment.objects.filter(
            nes_id=self.kwargs.get('pk2'), owner=self.request.user
        ).get()
        serializer.save(software_version=software_version,
                        experiment=experiment,
                        owner=self.request.user)


class ProtocolComponentList(generics.ListCreateAPIView):
    queryset = ProtocolComponent.objects.all()
    serializer_class = ProtocolComponentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        experiment = Experiment.objects.filter(
            nes_id=self.kwargs.get('pk'), owner=self.request.user
        ).get()
        serializer.save(experiment=experiment, owner=self.request.user)


class GroupList(generics.ListCreateAPIView):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        protocol_component = ProtocolComponent.objects.filter(
            nes_id=self.kwargs.get('pk'), owner=self.request.user
        ).get()
        serializer.save(protocol_component=protocol_component,
                        owner=self.request.user)


class ParticipantList(generics.ListCreateAPIView):
    queryset = Participant.objects.all()
    serializer_class = ParticipantSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class ExamFileList(generics.ListCreateAPIView):
    queryset = ExamFile.objects.all()
    serializer_class = ExamFileSerializer
    parser_classes = (parsers.MultiPartParser, parsers.FormParser)
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(content=self.request.data.get('content'),
                        owner=self.request.user)
