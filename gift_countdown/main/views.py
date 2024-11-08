from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from .decorators import can_view_gift
from django.contrib import messages
from django.urls import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden
from .forms import UserForm, GiftForm

from django.contrib.auth.models import User
from .models import GiftCountdown, Gift

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:  # Redirect staff users (admins) to the dashboard
                return redirect('admin_dashboard')
            else:  # Redirect regular users to the countdown page
                return redirect('user_countdown')
        else:
            messages.error(request, "Invalid usearname or password.")
    return render(request, 'main/login.html')

@login_required
def admin_dashboard(request):
    user_form = UserForm()
    gift_form = GiftForm(request.POST or None, request.FILES or None)

    if request.method == 'POST':
        if 'add_user' in request.POST:
            user_form = UserForm(request.POST)
            if user_form.is_valid():
                user_form.save()
                messages.success(request, "User created successfully.")
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Error creating user.")
        
        elif 'add_gift' in request.POST:
            gift_form = GiftForm(request.POST, request.FILES)
            if gift_form.is_valid():
                gift_form.save()
                messages.success(request, "Gift countdown added successfully.")  # This message will now appear only on the admin dashboard
                return redirect('admin_dashboard')
            else:
                messages.error(request, "Error adding gift countdown: " + str(gift_form.errors))

    users = User.objects.all()
    gifts = GiftCountdown.objects.all()

    context = {
        'user_form': user_form,
        'gift_form': gift_form,
        'users': users,
        'gifts': gifts,
    }
    return render(request, 'main/admin_dashboard.html', context)



def login_view(request):
    # Clear any lingering messages before login
    storage = messages.get_messages(request)
    for _ in storage:
        pass  # Clear the message storage to avoid showing unintended messages on the login page

    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff:  # Redirect staff users (admins) to the dashboard
                return redirect('admin_dashboard')
            else:  # Redirect regular users to the countdown page
                return redirect('user_countdown')
        else:
            messages.error(request, "Invalid username or password.")
    return render(request, 'main/login.html')


@login_required
def user_countdown(request):
    gifts = GiftCountdown.objects.filter(recipient=request.user)
    return render(request, 'main/user_countdown.html', {'gifts': gifts})

@login_required
def delete_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return HttpResponseRedirect(reverse('admin_dashboard'))


@login_required
def view_gift(request, gift_id):
    # Check if the gift exists and if the current user is the recipient
    gift = get_object_or_404(GiftCountdown, id=gift_id, recipient=request.user)
    
    # Additional check if the gift is not yet available
    if not gift.is_available():
        return HttpResponseForbidden("Gift is not yet available.")
    
    return render(request, 'main/view_gift.html', {'gift': gift})


def gift_list(request):
    gifts = Gift.objects.filter(
        recipient=request.user
    ).order_by('countdown_date')
    
    return render(request, 'gifts/gift_list.html', {
        'gifts': gifts
    })


# View to delete a gift countdown
@login_required
def delete_gift(request, gift_id):
    gift = get_object_or_404(GiftCountdown, id=gift_id)
    if request.method == 'POST':
        gift.delete()
        return HttpResponseRedirect(reverse('admin_dashboard'))

def logout_view(request):
    logout(request)
    return redirect('login')
