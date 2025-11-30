# messaging/views.py

from django.contrib.auth.models import User
from django.shortcuts import redirect, render, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Message
from django.db.models import Prefetch


@login_required
@require_POST
def delete_user(request):
    """
    Allows the currently authenticated user to delete their account.
    Triggers the post_delete signal on the User model.
    """
    # 1. Ensure the user confirms the deletion (optional, but good practice)
    #    In a real application, you'd check a confirmation flag/password here.

    # Get the user instance to be deleted
    user = request.user

    # Log out the user before deletion (to prevent immediate login attempt post-deletion)
    from django.contrib.auth import logout

    logout(request)

    # 2. Delete the user
    # This call to .delete() is what triggers the post_delete signal.
    username = user.username
    user.delete()

    messages.success(
        request, f"Your account ({username}) has been successfully deleted."
    )

    # Redirect to the homepage or a public-facing page
    return redirect("home")  # Assuming you have a URL named 'home'


@login_required
def conversation_list(request):
    """
    Displays a list of all primary (non-reply) message threads
    where the current user is either the sender or receiver.

    Uses select_related and prefetch_related for optimization.
    """
    current_user = request.user

    # Define a Prefetch object to optimize fetching the *immediate* replies.
    # We select_related the sender of the reply within the prefetch for max efficiency.
    replies_prefetch = Prefetch(
        "replies",
        queryset=Message.objects.select_related("sender").order_by("timestamp"),
        to_attr="immediate_replies",
    )

    # 1. Query the primary messages (those without a parent)
    # 2. Filter where the current user is involved
    # 3. select_related('sender', 'receiver'): Fetches the User objects for
    #    sender and receiver in the initial query (single join query).
    # 4. prefetch_related(replies_prefetch): Fetches all immediate replies for
    #    ALL retrieved primary messages in one extra batch query (instead of N queries).

    threads = (
        Message.objects.filter(
            parent_message__isnull=True,  # Only get thread starters
            sender=current_user,
        )
        .select_related("sender", "receiver")
        .prefetch_related(replies_prefetch)
        .order_by("-timestamp")
    )

    context = {
        "threads": threads,
    }
    return render(request, "messaging/conversation_list.html", context)


# --- View to fetch a single thread and its full recursive structure ---


def get_thread_data_recursive(message):
    """
    A non-optimized recursive function to fetch ALL descendants of a message.
    Used for full display but incurs N+1 problem for deep threads.
    """
    data = {
        "id": message.pk,
        "content": message.content,
        "sender": message.sender.username,
        "timestamp": message.timestamp,
        "replies": [],
    }

    # Recursive call to fetch replies for this message
    for reply in message.replies.select_related("sender").all():
        data["replies"].append(get_thread_data_recursive(reply))

    return data


@login_required
def conversation_detail(request, message_id):
    """
    Displays a single thread, including all replies in a nested structure.
    """
    # Get the root message, ensuring the user is involved in the conversation
    root_message = get_object_or_404(
        Message.objects.select_related("sender", "receiver"),
        pk=message_id,
        parent_message__isnull=True,  # Must be a thread starter
        sender=request.user,  # Check the user context here
    )

    # Build the full recursive structure
    threaded_data = get_thread_data_recursive(root_message)

    context = {
        "root_message": root_message,
        "threaded_data": threaded_data,  # Use this in the template for rendering
    }
    return render(request, "messaging/conversation_detail.html", context)


@login_required
def unread_inbox(request):
    """
    Displays the user's unread inbox using the custom manager.
    """
    # 🌟 Optimized Query using the custom manager:
    unread_messages = Message.unread.for_user(request.user)

    context = {
        "messages": unread_messages,
        "unread_count": unread_messages.count(),
    }
    return render(request, "messaging/unread_inbox.html", context)
