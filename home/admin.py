from django.contrib import admin

# Register your models here.
from home.models import Setting, ContactMessage
from product.models import Comment


class SettingtAdmin(admin.ModelAdmin):
    list_display = ['title', 'company', 'update_at', 'status']


class ContactMessageAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'update_at', 'status']
    readonly_fields = ('name', 'subject', 'email', 'message', 'ip')
    list_filter = ['status']


class CommentAdmin(admin.ModelAdmin):
    list_display = ['subject', 'comment', 'status', 'create_at']
    list_filter = ['status']
    readonly_fields = ('subject', 'comment', 'ip', 'user', 'product', 'rate', 'id')


admin.site.register(Setting, SettingtAdmin)
admin.site.register(ContactMessage, ContactMessageAdmin)
admin.site.register(Comment, CommentAdmin)
