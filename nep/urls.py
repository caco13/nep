from django.conf.urls import url, include
from django.contrib import admin
from experiments import views
from experiments import api_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api_urls)),
    url(r'^$', views.home_page, name='home'),
    url(r'^experiments/(?P<experiment_id>[0-9]+)/$', views.experiment_detail,
        name='experiment_detail'),
    url(r'^experiments/(?P<experiment_id>[0-9]+)/versions/$',
        views.experiment_versions, name='experiment_versions'),
    url(r'^participants/$', views.participants_page, name='participants'),
]
