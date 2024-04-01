from django.contrib import admin
from .models import About
from django_summernote.admin import SummernoteModelAdmin


@admin.register(About)
class AboutAdmin(SummernoteModelAdmin):
    """ Register the about model and improve content field ux for the admin user"""
    summernote_fields = ('content',)
