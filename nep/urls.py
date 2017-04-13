from django.conf.urls import url, include
from django.contrib import admin
from experiments import api_urls
import experiments.urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api_urls)),
    url(r'^', include(experiments.urls)),
]
