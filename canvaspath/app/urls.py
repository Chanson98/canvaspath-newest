from django.conf.urls import include, url
from .views import *
from django.views.generic import TemplateView

app_name = 'app'

urlpatterns = [
    url('^$', login),
]