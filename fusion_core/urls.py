from django.contrib import admin
from django.urls import path, include


admin.site.site_header = "Lottery BOT"
admin.site.site_title = "Lottery Admin Portal"
admin.site.index_title = "Добро пожаловать в Lottery"



urlpatterns = [
    path('admin/', admin.site.urls),
]
