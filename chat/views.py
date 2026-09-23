from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import ChatRoom, ChatMessage
from products.models import Product
from django.db.models import Q
from django.http import JsonResponse
from django.template.loader import render_to_string
from accounts.models import CustomUser


@login_required
def start_chat(request, product_id):

    product = get_object_or_404(
        Product,
        id=product_id
    )

    if request.user == product.seller:

        return redirect("product_detail", product.id)

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

@login_required
def fetch_messages(request, room_id):

    room = get_object_or_404(
        ChatRoom,
        id=room_id
    )

    messages = room.messages.all()

    html = render_to_string(

        "chat/messages.html",

        {

            "messages": messages,

            "request": request

        }

    )

    return JsonResponse({

        "html": html

    })


@login_required
def my_chats(request):

    rooms = ChatRoom.objects.filter(

        Q(customer=request.user) |
        Q(seller=request.user)

    ).order_by("-created_at")

    return render(

        request,

        "chat/my_chats.html",

        {

            "rooms": rooms

        }

    )

@login_required
def chat_with_admin(request):

    admin = CustomUser.objects.filter(role="admin").first()

    if not admin:
        return redirect("home")

    room, created = ChatRoom.objects.get_or_create(

        customer=request.user,
        seller=admin,
        product=None

    )

    return redirect(
        "chat_room",
        room.id
    )