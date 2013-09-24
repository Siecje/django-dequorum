
from django.contrib import admin
from . import models

admin.site.register(models.Category)
admin.site.register(models.Forum)
admin.site.register(models.Thread)
admin.site.register(models.Post)

class ThreadAdminInline(admin.StackedInline):
    model = models.ThreadAdmin
    extra = 0

class ForumAdminInline(admin.StackedInline):
    model = models.Forum
    extra = 0

class Profile(admin.ModelAdmin):
    inlines = [
        ForumAdminInline,
        ThreadAdminInline,
    ]

admin.site.register(models.Profile, Profile)
admin.site.register(models.ThreadAdmin)
admin.site.register(models.ForumAdmin)

