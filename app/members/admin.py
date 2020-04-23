from django.contrib import admin

# Register your models here.
from members.models import User, RecentlyPostList


class UserAdmin(admin.ModelAdmin):
    search_fields = ('id', 'username',)


class RecentlyPostListAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user', 'post']


admin.site.register(User, UserAdmin)
admin.site.register(RecentlyPostList, RecentlyPostListAdmin)
