from django.shortcuts import render
from tracks.models import Track

def index(request):
    tracks = Track.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'tracks': tracks})
