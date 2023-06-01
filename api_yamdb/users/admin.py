from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import User


@admin.register(User)
class UserAdmin(ImportExportModelAdmin, admin.ModelAdmin):
    list_display = ('pk', 'username', 'email',
                    'first_name', 'last_name', 'password')
    search_fields = ('username',)
    list_filter = ('username',)
    empty_value_display = '-пусто-'
