from django.contrib import admin
from .models import Message, Notification


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("sender", "receiver", "timestamp", "content")
    list_filter = ("timestamp", "sender", "receiver")
    search_fields = ("content", "sender__username", "receiver__username")
    date_hierarchy = "timestamp"
    readonly_fields = ("timestamp",)


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ("user", "message", "is_read", "timestamp")
    list_filter = ("is_read", "timestamp", "user")
    search_fields = ("content", "user__username")
    readonly_fields = ("timestamp",)
    actions = ["mark_as_read", "mark_as_unread"]

    @admin.action(description="Mark selected notifications as read")
    def mark_as_read(self, request, queryset):
        queryset.update(is_read=True)

    @admin.action(description="Mark selected notifications as unread")
    def mark_as_unread(self, request, queryset):
        queryset.update(is_read=False)
