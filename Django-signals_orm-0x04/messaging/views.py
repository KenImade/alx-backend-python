# messaging/views.py

from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST


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


# Conceptual Python/View Code:

# 1. Fetching Top-Level Messages (Thread Starters)
#    - Select the sender/receiver users in one go (select_related)
thread_starters = (
    Message.objects.filter(parent_message__isnull=True)
    .select_related("sender", "receiver")
    .order_by("-timestamp")
)


# 2. Fetching Replies for a Specific Thread (Recursive Pre-fetching)
#    - This is the most efficient way to fetch all direct replies to a message.
def get_thread_data(thread_id):
    """
    Fetches a specific message and its immediate replies efficiently.
    """
    try:
        # select_related: Fetches parent_message, sender, and receiver in one JOIN
        # prefetch_related: Fetches all immediate 'replies' in a separate batch query
        main_message = (
            Message.objects.select_related("parent_message", "sender", "receiver")
            .prefetch_related(
                "replies__sender"  # Pre-fetch the sender of the replies too!
            )
            .get(pk=thread_id)
        )

        return main_message

    except Message.DoesNotExist:
        return None


# Access: main_message.replies.all() will now be loaded in memory (cached).
