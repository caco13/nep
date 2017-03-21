from rest_framework import serializers, generics, permissions
from experiments.models import Experiment, Study, User, Researcher, \
    TMSSetting, EEGSetting, Manufacturer, Software, SoftwareVersion, EMGSetting
from experiments.permissions import IsOwnerOrReadOnly


# API Serializers
class ExperimentSerializer(serializers.ModelSerializer):
    study = serializers.ReadOnlyField(source='study.title')
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Experiment
        fields = ('id', 'title', 'description', 'data_acquisition_done',
                  'study', 'owner')


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


# API Views
class ExperimentList(generics.ListCreateAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(
            owner=self.request.user, study_id=self.kwargs.get('pk')
        )


class ExperimentDetail(generics.RetrieveUpdateAPIView):
    queryset = Experiment.objects.all()
    serializer_class = ExperimentSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly)


class UserList(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class StudyList(generics.ListCreateAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(researcher_id=self.kwargs.get('pk'))

    # TODO: não mostra estudos de um determinado pesquisador
    # def get(self, request, *args, **kwargs):
    #     study = self.get_object()
    #     return Response(study.researcher)


class StudyDetail(generics.RetrieveUpdateAPIView):
    queryset = Study.objects.all()
    serializer_class = StudySerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ResearcherList(generics.ListCreateAPIView):
    queryset = Researcher.objects.all()
    serializer_class = ResearcherSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ResearcherDetail(generics.RetrieveUpdateAPIView):
    queryset = Researcher.objects.all()
    serializer_class = ResearcherSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class TMSSettingList(generics.ListCreateAPIView):
    queryset = TMSSetting.objects.all()
    serializer_class = TMSSettingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(experiment_id=self.kwargs.get('pk'))


class TMSSettingDetail(generics.RetrieveUpdateAPIView):
    queryset = TMSSetting.objects.all()
    serializer_class = TMSSettingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class EEGSettingList(generics.ListCreateAPIView):
    queryset = EEGSetting.objects.all()
    serializer_class = EEGSettingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(experiment_id=self.kwargs.get('pk'))


class EEGSettingDetail(generics.RetrieveUpdateAPIView):
    queryset = EEGSetting.objects.all()
    serializer_class = EEGSettingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ManufacturerList(generics.ListCreateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class ManufacturerDetail(generics.RetrieveUpdateAPIView):
    queryset = Manufacturer.objects.all()
    serializer_class = ManufacturerSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class SoftwareList(generics.ListCreateAPIView):
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(manufacturer_id=self.kwargs.get('pk'))


class SoftwareDetail(generics.RetrieveUpdateAPIView):
    queryset = Software.objects.all()
    serializer_class = SoftwareSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class SoftwareVersionList(generics.ListCreateAPIView):
    queryset = SoftwareVersion.objects.all()
    serializer_class = SoftwareVersionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(software_id=self.kwargs.get('pk'))


class SoftwareVersionDetail(generics.RetrieveUpdateAPIView):
    queryset = SoftwareVersion.objects.all()
    serializer_class = SoftwareVersionSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)


class EMGSettingList(generics.ListCreateAPIView):
    queryset = EMGSetting.objects.all()
    serializer_class = EMGSettingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)

    def perform_create(self, serializer):
        serializer.save(software_version_id=self.kwargs.get('pk1'),
                        experiment_id=self.kwargs.get('pk2'))


class EMGSettingDetail(generics.RetrieveUpdateAPIView):
    queryset = EMGSetting.objects.all()
    serializer_class = EMGSettingSerializer
    permission_classes = (permissions.IsAuthenticatedOrReadOnly,)
