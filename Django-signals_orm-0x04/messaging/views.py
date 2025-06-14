from django.shortcuts import render, get_object_or_404, redirect
from .models import Message, MessageHistory
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import User
from django.http import HttpResponseForbidden
from django.views.decorators.http import require_POST
from django.contrib import messages
from django.contrib.auth import logout
from django.db.models import Prefetch


def message_history(request, message_id):
    message = get_object_or_404(Message, pk=message_id)
    history = message.history.all().order_by('-edited_at')
    
    return render(request, 'messaging/message_history.html', {
        'message': message,
        'history': history
    })

@login_required
def message_list(request):
    # Get all messages for the current user
    messages = Message.objects.filter(
        models.Q(receiver=request.user) | 
        models.Q(sender=request.user)
    ).order_by('-timestamp')
    
    return render(request, 'messaging/message_list.html', {
        'messages': messages
    })

@login_required
def post_message(request):
    if request.method == 'POST':
        receiver_id = request.POST.get('receiver')
        content = request.POST.get('content')
        
        try:
            receiver = User.objects.get(id=receiver_id)
            Message.objects.create(
                sender=request.user,
                receiver=receiver,
                content=content
            )
            return redirect('messaging:message_list')
        except User.DoesNotExist:
            return render(request, 'messaging/post_message.html', {
                'error': 'Invalid recipient'
            })
    
    # GET request - show form
    users = User.objects.exclude(id=request.user.id)
    return render(request, 'messaging/post_message.html', {
        'users': users
    })

@login_required
def message_detail(request, pk):
    message = get_object_or_404(Message, pk=pk)
    # Verify user has permission to view this message
    if message.sender != request.user and message.receiver != request.user:
        return HttpResponseForbidden()
    
    return render(request, 'messaging/message_detail.html', {
        'message': message
    })

@login_required
def edit_message(request, pk):
    message = get_object_or_404(Message, pk=pk, sender=request.user)
    
    if request.method == 'POST':
        message.content = request.POST.get('content')
        message.save()
        return redirect('messaging:message_detail', pk=message.id)
    
    return render(request, 'messaging/edit_message.html', {
        'message': message
    })

@login_required
def delete_user_confirm(request):
    """Show account deletion confirmation page"""
    return render(request, 'messaging/delete_account.html')


@login_required
@require_POST
def delete_user(request):
    """View to handle user account deletion"""
    user = request.user
    logout(request)
    user.delete()  # This will trigger the post_delete signal
    messages.success(request, 'Your account has been successfully deleted.')
    return redirect('home')  # Redirect to your home page


def conversation_thread(request, message_id):
    """Get the base message with alll replies efficeintly"""
    base_message = get_object_or_404(
        Message.objects.select_related('sender', 'receiver')
                        .prefetch_related(
                            Prefetch('replies',
                                     queryset=Message.objects.select_related('sender', 'receiver')),
                        ),
                        pk=message_id
    )
    return render(request, 'messaging/thread.html',{
        'base_message':  base_message,
        'thread_messages': base_message.get_thread()
    })


@login_required
def create_reply(request, parent_id):
    parent_message = get_object_or_404(Message, pk=parent_id)
    
    if request.method == 'POST':
        content = request.POST.get('content', '').strip()
        if content:
            Message.objects.create(
                sender=request.user,
                receiver=parent_message.sender if request.user == parent_message.receiver else parent_message.receiver,
                content=content,
                parent_message=parent_message
            )
            messages.success(request, 'Reply sent successfully.')
            return redirect('messaging:conversation_thread', message_id=parent_id)
    
    return redirect('messaging:conversation_thread', message_id=parent_id)
