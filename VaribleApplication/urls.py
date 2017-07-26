from django.conf.urls import url

from . import views

#this sheet defines the links to where all of the functions will live
#so this erally just needs to send the things to views.
urlpatterns = [
    url(r'^$', views.index, name='index'),
    #url(r'^tools/$', views.tools, name='tools'), #thinking...
    url(r'^(?P<func>.+)$', views.runapp), #for now we are going to capture everything
]