from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import Contact, ReachOut


@admin.register(Contact)
class ContactAdmin(SummernoteModelAdmin):
    """
    Adds rich-text editing of content in admin
    """
    summernote_fields = ('content',)

@admin.register(ReachOut)
class ReachOutAdmin(admin.ModelAdmin):
    list_display = ('message', 'read',)
