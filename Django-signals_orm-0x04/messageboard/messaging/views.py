from django.shortcuts import render, get_object_or_404, redirect
from .models import Message, MessageHistory
from django.contrib.auth.decorators import login_required
from django.db import models
from .models import User
from django.http import HttpResponseForbidden

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
