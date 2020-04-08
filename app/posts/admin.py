from django.contrib import admin

# Register your models here.

from posts.models import SalesForm, PostAddress, SecuritySafetyFacilities, PostRoom, AdministrativeDetail, \
    MaintenanceFee, RoomOption, RoomSecurity, PostTest


class PostRoomAdmin(admin.ModelAdmin):
    list_display = ['pk']


class SalesFormAdmin(admin.ModelAdmin):
    list_display = ['pk', 'type', 'depositChar', 'monthlyChar', 'depositInt', 'monthlyInt', ]


class AdministrativeDetailAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']


class PostAddressAdmin(admin.ModelAdmin):
    list_display = ['pk', 'loadAddress']


class SecuritySafetyFacilitiesAdmin(admin.ModelAdmin):
    list_display = ['pk', 'name']


class MaintenanceFeeAdmin(admin.ModelAdmin):
    list_display = ['pk', ]


class RoomOptionAdmin(admin.ModelAdmin):
    list_display = ['pk']


class RoomSecurityAdmin(admin.ModelAdmin):
    list_display = ['pk']


class PostTestAdmin(admin.ModelAdmin):
    list_display = ['pk', 'testtitle'
                    ]


admin.site.register(PostRoom, PostRoomAdmin)
admin.site.register(SalesForm, SalesFormAdmin)
admin.site.register(PostAddress, PostAddressAdmin)
admin.site.register(SecuritySafetyFacilities, SecuritySafetyFacilitiesAdmin)

admin.site.register(AdministrativeDetail, AdministrativeDetailAdmin)
admin.site.register(MaintenanceFee, MaintenanceFeeAdmin)
admin.site.register(RoomOption, RoomOptionAdmin)
admin.site.register(RoomSecurity, RoomSecurityAdmin)

admin.site.register(PostTest, PostTestAdmin)
