from django.conf.urls import url
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.schemas import get_schema_view
from experiments import api


schema_view = get_schema_view(title='NEP API')

urlpatterns = format_suffix_patterns([
    url(r'^schema/$', schema_view),
    url(r'^$', api.api_root),

    # researchers
    url(r'^researchers/$', api.ResearcherList.as_view(),
        name='api_researchers'),
    url(r'^researchers/(?P<nes_id>[0-9]+)/$', api.ResearcherListNesId.as_view(),
        name='api_researchers_nes_id'),
    url(r'^researchers/(?P<pk>[0-9]+)/update/$',
        api.ResearcherDetail.as_view()),

    # studies
    url(r'^studies/$', api.StudyList.as_view(), name='api_studies'),
    url(r'^researchers/(?P<pk>[0-9]+)/studies/$', api.StudyList.as_view(),
        name='api_studies_post'),
    url(r'^studies/(?P<nes_id>[0-9]+)/$', api.StudyListNesId.as_view()),
    url(r'^studies/(?P<pk>[0-9]+)/update/$', api.StudyDetail.as_view()),

    # experiments
    url(r'^experiments/$', api.ExperimentList.as_view(),
        name='api_experiments'),
    url(r'^studies/(?P<pk>[0-9]+)/experiments/$',
        api.ExperimentList.as_view(), name='api_experiments_post'),
    url(r'^experiments/(?P<nes_id>[0-9]+)/$',
        api.ExperimentListNesId.as_view()),
    url(r'^experiments/(?P<pk>[0-9]+)/update/$',
        api.ExperimentDetail.as_view()),

    url(r'^experiments/(?P<pk>[0-9]+)/tms_settings/$',
        api.TMSSettingList.as_view()),
    url(r'^tms_settings/$', api.TMSSettingList.as_view()),
    url(r'^experiments/(?P<pk>[0-9]+)/eeg_settings/$',
        api.EEGSettingList.as_view()),
    url(r'^eeg_settings/$', api.EEGSettingList.as_view()),
    url(r'^manufacturers/$', api.ManufacturerList.as_view()),
    url(r'^manufacturers/(?P<pk>[0-9]+)/softwares/$',
        api.SoftwareList.as_view()),
    url(r'^softwares/$', api.SoftwareList.as_view()),
    url(r'^softwares/(?P<pk>[0-9]+)/software_versions/$',
        api.SoftwareVersionList.as_view()),
    url(r'^software_versions/$', api.SoftwareVersionList.as_view()),
    url(r'^experiments/(?P<pk1>[0-9]+)/software_versions/(?P<pk2>['
        r'0-9]+)/emg_settings/$', api.EMGSettingList.as_view()),
    url(r'^emg_settings/$', api.EMGSettingList.as_view()),

    # protocol components
    url(r'^experiments/(?P<pk>[0-9]+)/protocol_components/$',
        api.ProtocolComponentList.as_view()),
    url(r'^protocol_components/$', api.ProtocolComponentList.as_view()),
    url(r'^protocol_components/(?P<pk>[0-9]+)/update/$',
        api.ProtocolComponentDetail.as_view()),

    url(r'^protocol_components/(?P<pk>[0-9]+)/groups/$',
        api.GroupList.as_view(), name='api_groups_post'),
    url(r'^groups/$', api.GroupList.as_view(), name='api_groups'),
    url(r'^participants/$', api.ParticipantList.as_view(),
        name='api_participants'),
    url(r'^exam_uploads/$', api.ExamFileList.as_view()),
])
