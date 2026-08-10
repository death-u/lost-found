from django.shortcuts import render

# Create your views here.
# basic function to render the index.html template
def index(request):
    return render(request, 'files/index.html');

# found logic to render the found_items.html template
def found(request):
    return render(request, 'files/found_items.html');

def lost(request):
    return render(request,'files/lost_items.html');