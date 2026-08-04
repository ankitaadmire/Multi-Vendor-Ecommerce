from django.urls import path
from . import views


urlpatterns = [

    path(
        'get-notifications/',
        views.get_notifications,
        name='get_notifications'
    ),
    
    path(
        "count/",
        views.notification_count,
        name="notification_count",
    ),

    path(
        "get-notifications/",
        views.get_notifications,
        name="get_notifications"
    ),

]