from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, Post, Notice

class NoticeAdmin(admin.ModelAdmin): # 공지사항 admin관리
    list_display = ('title', 'content', 'author', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at',)


class PostAdmin(admin.ModelAdmin): # 게시판 admin관리
    list_display = ('title', 'content', 'author', 'created_at')
    search_fields = ('title', 'content')
    readonly_fields = ('created_at',)

class AccountAdmin(BaseUserAdmin):
    list_display = ('email', 'username', 'name', 'create_at', 'last_login', 'is_admin', 'is_staff', 'university', 'major', 'address')
    search_fields = ('email', 'username', 'name')
    readonly_fields = ('id', 'create_at', 'last_login')

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(User, AccountAdmin)
admin.site.register(Post, PostAdmin)
admin.site.register(Notice, NoticeAdmin)
