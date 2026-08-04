from django.shortcuts import render, redirect, get_object_or_404

from django.contrib.auth.decorators import login_required

from .models import ChatRoom, ChatMessage

from products.models import Product


@login_required
def start_chat(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    room, created = ChatRoom.objects.get_or_create(

        customer=request.user,

        seller=product.seller,

        product=product

    )

    return redirect(
        "chat_room",
        room.id
    )


@login_required
def chat_room(request, room_id):

    room = get_object_or_404(
        ChatRoom,
        id=room_id
    )

    if request.method == "POST":

        message = request.POST.get("message")

        if message:

            ChatMessage.objects.create(

                room=room,

                sender=request.user,

                message=message

            )

        return redirect(
            "chat_room",
            room.id
        )

    messages = room.messages.all()

    return render(

        request,

        "chat/chat_room.html",

        {

            "room": room,

            "messages": messages

        }

    )