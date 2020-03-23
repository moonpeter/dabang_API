from django.contrib import admin

# Register your models here.
from members.models import User


class UserAdmin(admin.ModelAdmin):
    search_fields = ('id', 'username',)


admin.site.register(User, UserAdmin)
