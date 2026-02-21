from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from accounts.models import CustomUser
from .models import Message
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Q



# Create your views here.
def index(request):
    if request.user.is_authenticated:
        return redirect('user_list')
    return render(request, 'index.html')

@login_required
def user_list(request):
    users = CustomUser.objects.exclude(id=request.user.id)
    return render(request, "user_list.html", {"users": users})

@login_required
def chat(request, username):
    other_user = get_object_or_404(CustomUser, username=username)

    # Get all messages between users
    messages = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).select_related('sender', 'receiver').order_by("timestamp")

    return render(request, "chat.html", {
        "other_user": other_user,
        "messages": messages
    })

@login_required
@require_POST
def mark_messages_read(request, username):
    """API endpoint to mark messages as read"""
    other_user = get_object_or_404(CustomUser, username=username)
    
    # Mark all unread messages from other user as read
    updated = Message.objects.filter(
        sender=other_user,
        receiver=request.user,
        is_read=False
    ).update(is_read=True)
    
    return JsonResponse({
        'status': 'success',
        'marked_read': updated
    })

