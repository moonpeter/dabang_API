from django.contrib import admin

# Register your models here.
from django.contrib.auth import get_user_model

from members.models import SocialLogin
from posts.models import SalesForm

User = get_user_model()


class UserAdmin(admin.ModelAdmin):
    search_fields = ('id', 'username', 'social')
    list_display = ['id', 'username']

    # def social(self, obj):
    #     return ' '.join([])


class SocialLoginAdmin(admin.ModelAdmin):
    list_display = ['pk', 'type']


class SalesFormAdmin(admin.ModelAdmin):
    list_display = ['pk', 'type']


admin.site.register(User, UserAdmin)
admin.site.register(SocialLogin, SocialLoginAdmin)
admin.site.register(SalesForm, SalesFormAdmin)
