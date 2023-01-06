from django.contrib import admin

from .views import Gator, Comment

admin.site.register(Gator)
admin.site.register(Comment)
