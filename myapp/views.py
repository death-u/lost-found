from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from . import vision_ai
from .models import FoundItem
from django.contrib import messages
import json

# Create your views here.
# basic function to render the index.html template
def index(request):
    return render(request, 'files/index.html');

# found logic to render the found_items.html template


def found(request):
    if request.method == 'POST':
        item_image1 = request.FILES.get('item_image')
        title1 = request.POST.get('title')
        category1 = request.POST.get('category')
        location1 = request.POST.get('location')
        description1 = request.POST.get('description')
        ai_data_raw = request.POST.get('ai_data', '{}')

        if not item_image1 or not title1:
            messages.error(request, 'Title and image are required.')
            return redirect('found_items')
        if not category1 or not location1:
            messages.error(request, 'Category and where the item was found are required.')
            return redirect('found_items')

        try:
            ai_data = json.loads(ai_data_raw)
        except json.JSONDecodeError:
            ai_data = {}

        FoundItem.objects.create(
            title=title1,
            category=category1,
            location=location1,
            image=item_image1,
            description=description1,
            primary_color=ai_data.get('primary_color', ''),
            secondary_colors=ai_data.get('secondary_colors', []),
            material=ai_data.get('material'),
            distinguishing_features=ai_data.get('distinguishing_features', []),
            brand=ai_data.get('brand'),
        )
        messages.success(request, 'Item submitted successfully!')
        return redirect('found_items')

    return render(request, 'files/found_items.html')

# basic function to render the index.html template
def lost(request):
    selected_category = request.GET.get('category', 'all')
    search_query = request.GET.get('q', '').strip()

    # Get distinct categories from database
    categories = FoundItem.objects.exclude(category='').values_list('category', flat=True).distinct()

    # Base Queryset ordered by newest first
    items = FoundItem.objects.all().order_by('-date_found')

    # Apply category filter
    if selected_category and selected_category != 'all':
        items = items.filter(category__iexact=selected_category)

    # Apply search query filter
    if search_query:
        items = items.filter(title__icontains=search_query)

    context = {
        "items": items,
        "categories1": categories,
        "selected_category": selected_category,
        "search_query": search_query,
    }
    return render(request,'files/lost_items.html', context);

@require_POST
def detect(request):
    uploaded_image = request.FILES.get('image') # or request.FILES.get('item_image')

    if not uploaded_image:
        return JsonResponse({
            'success': False, 
            'error': 'No image file was received.'
        }, status=400)

    # ai logic here
    # generate(uploaded_image,"des")
    response = vision_ai.analyze_item(uploaded_image)
    print(response)  # Log the response for debugging purposes
    # Mock detected result to send back to frontend JS
    detected_title =response['item_type'] or "Black Leather School Bag success"
    detected_category = response['category'] or "Bags & Backpacks success"

    return JsonResponse({
        'success': True,
        'title': detected_title,
        'category': detected_category,
        'data': response
    })