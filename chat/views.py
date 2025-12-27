from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import SignupForm
from .models import Channel, Message

def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
    else:
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})

@login_required
def index(request, channel_name=None):
    channels = Channel.objects.all()
    current_channel = None
    messages = []
    
    if channel_name:
        current_channel = get_object_or_404(Channel, name=channel_name)
        messages = Message.objects.filter(channel=current_channel).order_by('created_at')
    
    return render(request, 'chat/index.html', {
        'channels': channels,
        'current_channel': current_channel,
        'messages': messages,
        'room_name': current_channel.name if current_channel else None
    })
