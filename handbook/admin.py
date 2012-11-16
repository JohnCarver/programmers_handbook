# coding: utf-8

from django.contrib import admin
from handbook.models import Node, Content


class ContentInline(admin.TabularInline):
    model = Content
    extra = 2


class NodeAdmin(admin.ModelAdmin):
    list_display = ('title', 'parent', 'updated_at', 'created_at', 'created_by')
    list_filter = ['created_by']
    search_fields = ['title']
    date_hierarchy = 'updated_at'
    ordering = ('-updated_at',)
    inlines = [
        ContentInline,
    ]


admin.site.register(Node, NodeAdmin)


class ContentAdmin(admin.ModelAdmin):
    list_display = ('node', 'version', 'created_at', 'created_by')
    list_filter = ['created_by']
    search_fields = ['text']
    ordering = ('-created_at',)


admin.site.register(Content, ContentAdmin)
