from django.conf.urls import url

from experiments import views

urlpatterns = [
    url(r'^experiments/$', views.home_page, name='home'),
    url(r'^experiments/(?P<experiment_id>[0-9]+)/$', views.experiment_detail,
        name='experiment_detail'),
    url(r'^experiments/(?P<experiment_id>[0-9]+)/versions/$',
        views.experiment_versions, name='experiment_versions'),
    url(r'^experiments/(?P<experiment_id>[0-9]+)/versions/(?P<version>['
        r'0-9]+)/$', views.experiment_version_detail,
        name='experiment_version_detail'),
    url(r'^experiments/(?P<experiment_id>[0-9]+)/versions/(?P<version>['
        r'0-9]+)/study$', views.experiment_study_version,
        name='experiment_study_version'),
    url(r'^experiments/(?P<experiment_id>[0-9]+)/study/$',
        views.experiment_study, name='experiment_study'),
    url(r'^participants/$', views.participants_page, name='participants'),
]
