from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import UserRegisterForm, SwagForm, SwagSearchForm
from .models import Swag

# Create your views here.
def home(request):
    """Home page view showing recent swags and search functionality"""
    search_form = SwagSearchForm(request.GET or None)
    swags = Swag.objects.all()

    # Handle search
    if search_form.is_valid() and search_form.cleaned_data.get('query'):
        query = search_form.cleaned_data.get('query')
        swags = swags.filter(
            Q(name__icontains=query) | 
            Q(company__icontains=query) | 
            Q(conference__icontains=query) |
            Q(comments__icontains=query)
        )

    context = {
        'swags': swags,
        'search_form': search_form,
    }
    return render(request, 'swags/home.html', context)

def register(request):
    """User registration view"""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'registration/register.html', {'form': form})

@login_required
def swag_create(request):
    """View for creating a new swag item"""
    if request.method == 'POST':
        form = SwagForm(request.POST, request.FILES)
        if form.is_valid():
            swag = form.save(commit=False)
            swag.user = request.user
            swag.save()
            messages.success(request, 'Your swag has been added!')
            return redirect('swag_detail', pk=swag.pk)
    else:
        form = SwagForm()
    return render(request, 'swags/swag_form.html', {'form': form, 'title': 'Add Swag'})

@login_required
def swag_update(request, pk):
    """View for updating an existing swag item"""
    swag = get_object_or_404(Swag, pk=pk, user=request.user)
    if request.method == 'POST':
        form = SwagForm(request.POST, request.FILES, instance=swag)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your swag has been updated!')
            return redirect('swag_detail', pk=swag.pk)
    else:
        form = SwagForm(instance=swag)
    return render(request, 'swags/swag_form.html', {'form': form, 'title': 'Update Swag'})

def swag_detail(request, pk):
    """View for displaying a single swag item"""
    swag = get_object_or_404(Swag, pk=pk)
    return render(request, 'swags/swag_detail.html', {'swag': swag})

@login_required
def user_swags(request):
    """View for displaying the current user's swags"""
    swags = Swag.objects.filter(user=request.user)
    return render(request, 'swags/user_swags.html', {'swags': swags})
