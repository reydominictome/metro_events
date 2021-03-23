from django.urls import path, include
from . import views
from django.conf import settings
from django.conf.urls.static import static

app_name = 'webapp'

urlpatterns = [
    path('', views.MetroEventsIndexView.as_view(), name='landing'),
    path('home', views.MetroEventsHomeView.as_view(), name='home'),
    path('events', views.MetroEventsEventsView.as_view(), name='events'),
    path('events_registration', views.MetroEventsEventsRegistrationView.as_view(), name='events_registration'),
    path('administrator', views.MetroEventsAdministratorView.as_view(), name='administrator'),
    path('organizer', views.MetroEventsOrganizerView.as_view(), name='organizer'),
]