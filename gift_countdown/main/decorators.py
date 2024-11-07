from django.http import HttpResponseForbidden
from functools import wraps
from .models import GiftCountdown

def can_view_gift(view_func):
    @wraps(view_func)
    def _wrapped_view(request, gift_id, *args, **kwargs):
        # Check if the gift is associated with the current user
        gift = GiftCountdown.objects.filter(id=gift_id, recipient=request.user).first()
        if not gift:
            return HttpResponseForbidden("You do not have permission to view this gift.")
        # Pass the gift_id to the view function if permission is granted
        return view_func(request, gift_id=gift_id, *args, **kwargs)
    return _wrapped_view
