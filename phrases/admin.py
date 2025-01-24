from django.contrib import admin
from phrases.models import OnlyReplies


@admin.register(OnlyReplies)
class OnlyRepliesAdmin(admin.ModelAdmin):
    list_display = ('name', 'description','kaz','rus','updated_at')
    search_fields = ('name','description','kaz','rus')
    readonly_fields = ('updated_at',)
