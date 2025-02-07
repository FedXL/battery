from django.contrib import admin
from django.conf import settings
from phrases.models import OnlyReplies


@admin.register(OnlyReplies)
class OnlyRepliesAdmin(admin.ModelAdmin):
    list_display = ('name','is_checked','description','kaz','rus','updated_at')
    search_fields = ('name','description','kaz','rus')
    if settings.VERSION == 'deploy':
        readonly_fields = ('updated_at','name','description')



