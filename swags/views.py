from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from .forms import UserRegisterForm, SwagForm, SwagSearchForm, SwagCommentForm, SwagRatingForm
from .models import Swag, SwagComment, SwagRating

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
    """View for displaying a single swag item and handling comments and ratings"""
    swag = get_object_or_404(Swag, pk=pk)
    comments = SwagComment.objects.filter(swag=swag)
    user_rating = None

    # Initialize forms
    comment_form = None
    rating_form = None

    if request.user.is_authenticated:
        # Check if user has already rated this swag
        try:
            user_rating = SwagRating.objects.get(swag=swag, user=request.user)
            rating_form = SwagRatingForm(instance=user_rating)
        except SwagRating.DoesNotExist:
            rating_form = SwagRatingForm()

        comment_form = SwagCommentForm()

        # Handle comment submission
        if request.method == 'POST' and 'comment_submit' in request.POST:
            comment_form = SwagCommentForm(request.POST)
            if comment_form.is_valid():
                comment = comment_form.save(commit=False)
                comment.swag = swag
                comment.user = request.user
                comment.save()
                messages.success(request, 'Your comment has been added!')
                return redirect('swag_detail', pk=swag.pk)

        # Handle rating submission
        if request.method == 'POST' and 'rating_submit' in request.POST:
            if user_rating:
                rating_form = SwagRatingForm(request.POST, instance=user_rating)
            else:
                rating_form = SwagRatingForm(request.POST)

            if rating_form.is_valid():
                rating = rating_form.save(commit=False)
                rating.swag = swag
                rating.user = request.user
                rating.save()
                messages.success(request, 'Your rating has been saved!')
                return redirect('swag_detail', pk=swag.pk)

    context = {
        'swag': swag,
        'comments': comments,
        'comment_form': comment_form,
        'rating_form': rating_form,
        'user_rating': user_rating,
    }
    return render(request, 'swags/swag_detail.html', context)

@login_required
def user_swags(request):
    """View for displaying the current user's swags"""
    swags = Swag.objects.filter(user=request.user)
    return render(request, 'swags/user_swags.html', {'swags': swags})
