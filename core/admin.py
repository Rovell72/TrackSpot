from django.contrib import admin

from .models import StoredFile


@admin.register(StoredFile)
class StoredFileAdmin(admin.ModelAdmin):
    list_display = ('name', 'content_type', 'size', 'created_at')
    search_fields = ('name',)
    readonly_fields = ('name', 'content_type', 'size', 'created_at')
    exclude = ('content',)

    def get_queryset(self, request):
        # не тянем сами байты при показе списка
        return super().get_queryset(request).defer('content')

    def has_add_permission(self, request):
        return False
