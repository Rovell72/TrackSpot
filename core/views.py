from django.http import Http404, HttpResponse
from django.shortcuts import render
from django.views.decorators.http import require_safe

from tracks.models import Track
from .models import StoredFile
from .ranges import RangeNotSatisfiable, parse_range

# Всё остальное отдаём как скачиваемый octet-stream, чтобы загруженный файл
# не мог выполниться в браузере как HTML/SVG/JS.
SAFE_INLINE_TYPES = {
    'image/jpeg', 'image/png', 'image/gif', 'image/webp', 'image/bmp', 'image/avif',
    'audio/mpeg', 'audio/mp3', 'audio/wav', 'audio/x-wav', 'audio/wave',
    'audio/ogg', 'audio/flac', 'audio/x-flac', 'audio/mp4', 'audio/aac',
}


def index(request):
    tracks = Track.objects.all().order_by('-created_at')
    return render(request, 'index.html', {'tracks': tracks})


@require_safe
def media_file(request, name):
    """Отдаёт файл (аватарка / обложка / аудио) из базы данных."""
    try:
        meta = StoredFile.objects.defer('content').get(name=name)
    except StoredFile.DoesNotExist:
        raise Http404("Файл не найден")

    etag = f'"{meta.pk}-{meta.size}-{int(meta.created_at.timestamp())}"'
    headers = {
        'ETag': etag,
        'Cache-Control': 'public, max-age=3600',
        'Accept-Ranges': 'bytes',
        'X-Content-Type-Options': 'nosniff',
    }

    if request.headers.get('If-None-Match') == etag:
        return HttpResponse(status=304, headers=headers)

    if meta.content_type in SAFE_INLINE_TYPES:
        content_type = meta.content_type
    else:
        content_type = 'application/octet-stream'
        headers['Content-Disposition'] = 'attachment'

    data = bytes(StoredFile.objects.values_list('content', flat=True).get(pk=meta.pk))
    total = len(data)

    try:
        byte_range = parse_range(request.headers.get('Range'), total)
    except RangeNotSatisfiable:
        return HttpResponse(status=416, headers={**headers, 'Content-Range': f'bytes */{total}'})

    if byte_range:
        start, end = byte_range
        response = HttpResponse(data[start:end + 1], status=206, content_type=content_type, headers=headers)
        response['Content-Range'] = f'bytes {start}-{end}/{total}'
        return response

    return HttpResponse(data, content_type=content_type, headers=headers)
