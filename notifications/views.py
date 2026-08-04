from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import Notification
from django.template.loader import render_to_string



@login_required
def get_notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")[:5]


    unread_count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()


    notification_list = []


    for notification in notifications:

        notification_list.append({

            "message": notification.message,

            "time": notification.created_at.strftime(
                "%d %b %Y %H:%M"
            )

        })


    return JsonResponse({

        "count": unread_count,

        "notifications": notification_list

    })

@login_required
def notification_count(request):

    count = Notification.objects.filter(
        user=request.user,
        is_read=False
    ).count()

    return JsonResponse({
        "count": count
    })


@login_required
def get_notifications(request):

    notifications = Notification.objects.filter(
        user=request.user
    ).order_by("-created_at")[:5]

    html = render_to_string(
        "notifications/notification_list.html",
        {
            "notifications": notifications
        }
    )

    return JsonResponse({
        "html": html
    })