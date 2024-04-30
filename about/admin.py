from django.contrib import admin
from django_summernote.admin import SummernoteModelAdmin
from .models import About


@admin.register(About)
class AboutAdmin(SummernoteModelAdmin):
    """ Register the about model and improve content
    field ux for the admin user"""
    summernote_fields = ('content',)

