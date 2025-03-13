from django.urls import path,include
from . import views
from .views import EventViewSet,AtttendeeViewSet,UserViewSet
from rest_framework.routers import DefaultRouter
from django.http import HttpResponse

router = DefaultRouter()
router.register(r'events', EventViewSet, basename='event')
router.register(r'attendees', AtttendeeViewSet, basename='atendee')
router.register(r'users', UserViewSet, basename='user')




urlpatterns = [
    path('',views.home, name="home"),
    path('api/', include(router.urls)),
]
