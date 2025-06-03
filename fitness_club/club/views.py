from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.utils import timezone
from .models import Member, Membership, Service, Booking
from .forms import RegisterForm, MembershipForm, ProfileUpdateForm, BookingForm

def home(request):
    services = Service.objects.filter(available=True)[:3]
    return render(request, 'club/home.html', {'services': services})

def about(request):
    return render(request, 'club/about.html')

def services(request):
    services = Service.objects.filter(available=True)
    return render(request, 'club/services.html', {'services': services})

def service_detail(request, service_id):
    service = get_object_or_404(Service, id=service_id)
    
    if request.method == 'POST' and request.user.is_authenticated:
        form = BookingForm(request.POST)
        if form.is_valid():
            booking = form.save(commit=False)
            booking.user = request.user
            booking.service = service 
            booking.save()
            return redirect('profile')
    else:
        form = BookingForm(initial={'service': service})
    
    return render(request, 'club/service_detail.html', {
        'service': service,
        'form': form
    })

def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Member.objects.create(
                user=user,
                phone=form.cleaned_data['phone'],
                birth_date=form.cleaned_data['birth_date']
            )
            login(request, user)
            return redirect('profile')
    else:
        form = RegisterForm()
    return render(request, 'club/register.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            return render(request, 'club/login.html', {'error': 'Неверные данные для входа'})
    return render(request, 'club/login.html')

@login_required
def user_logout(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    try:
        member = request.user.member
    except Member.DoesNotExist:
        if request.user.is_staff:
            return redirect('/admin/')
        member = Member.objects.create(user=request.user)
    
    bookings = Booking.objects.filter(user=request.user).order_by('date', 'time')
    now = timezone.now()
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, request.FILES, instance=member)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = ProfileUpdateForm(instance=member)
    
    return render(request, 'club/profile.html', {
        'form': form,
        'member': member,
        'bookings': bookings,
        'now': now
    })

@login_required
def membership_list(request):
    memberships = Membership.objects.all()
    return render(request, 'club/memberships.html', {'memberships': memberships})

@login_required
def add_membership(request):
    if not request.user.is_staff:
        return redirect('home')
    
    if request.method == 'POST':
        form = MembershipForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('memberships')
    else:
        form = MembershipForm()
    
    return render(request, 'club/add_membership.html', {'form': form})