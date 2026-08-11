from django.shortcuts import render,redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from . import vision_ai

# Create your views here.
# basic function to render the index.html template
def index(request):
    return render(request, 'files/index.html');

# found logic to render the found_items.html template
def found(request):
    return render(request, 'files/found_items.html');

# basic function to render the index.html template
def lost(request):
    return render(request,'files/lost_items.html');

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