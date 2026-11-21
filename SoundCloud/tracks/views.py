from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from .models import Track
from .forms import TrackForm

@login_required
def upload_track(request):
    if request.user.profile.role != 'artist':
        return render(request, 'tracks/access_denied.html')

    if request.method == 'POST':
        form = TrackForm(request.POST, request.FILES)
        if form.is_valid():
            track = form.save(commit=False)
            track.author = request.user
            track.save()
            return redirect('home')
    else:
        form = TrackForm()
    
    return render(request, 'tracks/track_form.html', {'form': form, 'title': 'Загрузить трек'})

@login_required
def edit_track(request, pk):
    track = get_object_or_404(Track, pk=pk)
    if track.author != request.user:
        return HttpResponseForbidden("Вы не можете редактировать чужой трек.")

    if request.method == 'POST':
        form = TrackForm(request.POST, request.FILES, instance=track)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = TrackForm(instance=track)

    return render(request, 'tracks/track_form.html', {'form': form, 'title': 'Редактировать трек'})

@login_required
def delete_track(request, pk):
    track = get_object_or_404(Track, pk=pk)
    if track.author != request.user:
        return HttpResponseForbidden("Вы не можете удалить чужой трек.")

    if request.method == 'POST':
        track.delete()
        return redirect('home')

    return render(request, 'tracks/track_confirm_delete.html', {'track': track})
