from django.contrib import admin
from .models import Contact, ReachOut
from django_summernote.admin import SummernoteModelAdmin


@admin.register(Contact)
class ContactAdmin(SummernoteModelAdmin):
    """
    Adds rich-text editing of content in admin
    """
    summernote_fields = ('content',)

@admin.register(ReachOut)
class ReachOutAdmin(admin.ModelAdmin):
    list_display = ('message', 'read',)
