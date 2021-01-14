def users_disable(modeladmin, request, queryset):
    queryset.update(is_active=False)


def users_enable(modeladmin, request, queryset):
    queryset.update(is_active=True)


users_disable.short_description = "Деактивировать выбранных пользователей"
users_enable.short_description = "Активировать выбранных пользователей"
