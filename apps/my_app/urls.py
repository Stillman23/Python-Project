from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^registration_process$', views.registration_process),
    url(r'^login_process$', views.login_process),
    url(r'^travels$', views.travels),
    url(r'^addplan$', views.addplan),
    url(r'^logout$', views.logout),
     url(r'^createplan$', views.createplan),
    url(r'^show/(?P<travel_id>\d+)$', views.show),
    url(r'^join/(?P<travel_id>\d+)$', views.join),
    url(r'^delete/(?P<id>\d+)$', views.delete)
]