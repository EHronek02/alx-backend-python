from django.contrib import admin
from .models import Message, Notification, MessageHistory


class MessageHistoryInline(admin.TabularInline):
    model = MessageHistory
    extra = 0
    readonly_fields = ('edited_at', 'edited_by', 'old_content')
    can_delete = False

    def has_add_permission(self, request, obj=None):
        return False
    

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('sender', 'receiver', 'timestamp', 'is_read', 'is_edited')
    list_filter = ('is_read', 'is_edited', 'timestamp')
    search_fields = ('content', 'sender__username', 'receiver__username')
    inlines = [MessageHistoryInline]


@admin.register(MessageHistory)
class MessageHistoryAdmin(admin.ModelAdmin):
    list_display = ('message', 'edited_by', 'edited_at')
    readonly_fields = ('message', 'old_content', 'edited_by', 'edited_at')
    list_filter = ('edited_at',)
    search_fields = ('message__content', 'old_content')


@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ('user', 'message', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('user__username', 'message__content')

    
