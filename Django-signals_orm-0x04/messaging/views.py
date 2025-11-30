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
    user_to_delete = request.user

    # Log out the user before deletion (to prevent immediate login attempt post-deletion)
    from django.contrib.auth import logout

    logout(request)

    # 2. Delete the user
    # This call to .delete() is what triggers the post_delete signal.
    username = user_to_delete.username
    user_to_delete.delete()

    messages.success(
        request, f"Your account ({username}) has been successfully deleted."
    )

    # Redirect to the homepage or a public-facing page
    return redirect("home")  # Assuming you have a URL named 'home'
