from django.conf.urls import url, include
from django.contrib import admin
from experiments import views
from experiments import api_urls

urlpatterns = [
    url(r'^$', views.home_page, name='home'),
    url(r'^participants/$', views.participants_page, name='participants'),
    url(r'^admin/', admin.site.urls),
    url(r'^api/', include(api_urls)),
]
