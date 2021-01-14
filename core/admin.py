from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as DefaultUserAdmin
from django.utils.translation import gettext_lazy as _

from core.admin_actions import users_disable, users_enable
from core.models import User, Restaurant, RestaurantImage, Place, Reservation

from import_export.admin import ImportExportModelAdmin


class UserAdmin(DefaultUserAdmin):
    list_display = ('email', 'name', 'is_active', 'is_superuser', 'is_staff', 'token_field')
    list_filter = ('is_active', 'is_superuser', 'is_staff', )

    search_fields = ('email', 'name')
    ordering = ('id',)

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'password1', 'password2'),
        }),
    )
    fieldsets = (
        (None, {'fields': ('email', 'name', 'password')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', )}),
    )

    actions = [users_disable, users_enable]

    def token_field(self, obj):
        return obj.auth_tokens.first()
    token_field.short_description = 'REST-токен'


class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('owner', 'name', 'city', 'address', 'phone', )


class RestaurantImageAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'image', )


class PlaceAdmin(admin.ModelAdmin):
    list_display = ('restaurant', 'hall_number', 'table_number', 'max_places', 'image', )


class ReservationAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('restaurant', 'place', 'reserved_at', 'created_at', 'get_phone_as_href', 'name', 'places', )
    list_filter = ('restaurant__name', 'reserved_at', )
    

admin.site.register(User, UserAdmin)
admin.site.register(Restaurant, RestaurantAdmin)
admin.site.register(RestaurantImage, RestaurantImageAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(Reservation, ReservationAdmin)
