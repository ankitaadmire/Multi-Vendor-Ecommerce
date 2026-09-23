from django.urls import path
from . import views

urlpatterns = [

    path(
        "start/<int:product_id>/",
        views.start_chat,
        name="start_chat"
    ),

    path(
        "room/<int:room_id>/",
        views.chat_room,
        name="chat_room"
    ),

    path(
        "my-chats/",
        views.my_chats,
        name="my_chats"
    ),

    path(
        "fetch/<int:room_id>/",
        views.fetch_messages,
        name="fetch_messages"
    ),

    path(
        "admin/",
        views.chat_with_admin,
        name="chat_with_admin"
    ),

]