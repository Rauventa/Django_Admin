from django.contrib import admin
from django.contrib.auth.models import Group, Permission

from authtoken.models import Token


class TokenAdmin(admin.ModelAdmin):
    list_display = ('key', 'user', 'created_at')
    fields = ('user',)
    ordering = ('-created_at',)


admin.site.register(Token, TokenAdmin)
admin.site.register(Permission)
