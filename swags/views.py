from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.http import JsonResponse
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

def get_suggestions(request):
    """API endpoint to provide suggestions for conference and company names"""
    query = request.GET.get('query', '')
    field = request.GET.get('field', '')

    if not query or not field or field not in ['conference', 'company']:
        return JsonResponse({'suggestions': []})

    # Get distinct values for the specified field that contain the query
    suggestions = Swag.objects.filter(**{f"{field}__icontains": query}) \
                             .values_list(field, flat=True) \
                             .distinct()

    # Remove duplicates case-insensitively
    unique_suggestions = []
    lower_suggestions = set()

    for suggestion in suggestions:
        if suggestion.lower() not in lower_suggestions:
            lower_suggestions.add(suggestion.lower())
            unique_suggestions.append(suggestion)

    # Limit to 10 suggestions
    unique_suggestions = unique_suggestions[:10]

    return JsonResponse({'suggestions': unique_suggestions})

def get_similar_swags(request):
    """API endpoint to find similar swags based on name, company, conference, and year"""
    name = request.GET.get('name', '').strip()
    company = request.GET.get('company', '').strip()
    conference = request.GET.get('conference', '').strip()
    year = request.GET.get('year', '').strip()

    # Return empty if no search criteria provided
    if not any([name, company, conference, year]):
        return JsonResponse({'similar_swags': []})

    # Start with all swags
    query = Swag.objects.all()

    # Apply filters based on provided fields
    if name:
        query = query.filter(name__icontains=name)
    if company:
        query = query.filter(company__icontains=company)
    if conference:
        query = query.filter(conference__icontains=conference)
    if year and year.isdigit():
        query = query.filter(year=int(year))

    # Get the similar swags with their details
    similar_swags = []
    for swag in query[:5]:  # Limit to 5 similar swags
        swag_data = {
            'id': swag.pk,
            'name': swag.name,
            'company': swag.company,
            'conference': swag.conference,
            'year': swag.year,
            'rating': swag.rating,
            'photo_url': swag.photo.url if swag.photo else None
        }
        similar_swags.append(swag_data)

    return JsonResponse({'similar_swags': similar_swags})
