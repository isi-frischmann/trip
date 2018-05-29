from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'^process$', views.process),
    url(r'^dashboard$', views.dashboard),
    url(r'^add_trip$', views.add_trip),
    url(r'^adding$', views.adding),
    url(r'^show_trip/(?P<trip_id>\d+)$', views.show_trip),
    url(r'^cancel_trip/(?P<trip_id>\d+)$', views.cancel),
    url(r'^delete/(?P<trip_id>\d+)$', views.delete),
    url(r'^join/(?P<trip_id>\d+)$', views.join),
    url(r'^back$', views.back),
    url(r'^logout$', views.logout)
]