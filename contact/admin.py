from django.contrib import admin
from .models import ReachOut
from django_summernote.admin import SummernoteModelAdmin


@admin.register(ReachOut)
class ReachOutAdmin(admin.ModelAdmin):
    list_display = ('message', 'read',)
