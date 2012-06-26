# -*- coding: utf-8 -*-

"""
Project: BugEx Online
Authors: Amir Baradaran
         Tim Krones
         Frederik Leonhardt
         Christos Monogios
         Akmal Qodirov
         Iliana Simova
         Peter Stahl
"""

from django.contrib import admin

from bugex_webapp.models import UserRequest, CodeArchive, TestCase, BugExResult
from bugex_webapp.models import Fact, Folder, SourceFile, ClassFile, Line
from bugex_webapp.models import MethodElement, FieldElement, ClassElement

class UserRequestAdmin(admin.ModelAdmin):
    """The admin site configuration for the UserRequest model."""
    fieldsets = (
        (None, {
            'fields': ('status', 'token')
        }),
        (None, {
            'fields': ('code_archive', 'result', 'test_case', 'user')
        })
    )
    list_display = ('status', 'token', 'code_archive', 'result', 'test_case', 'user')
    list_display_links = ('token',)
    list_filter = ('status', 'user__username')
    ordering = ('user', 'result')


class CodeArchiveAdmin(admin.ModelAdmin):
    """The admin site configuration for the CodeArchive model."""
    fields = ('archive_format', 'name')
    list_display = ('archive_format', 'name')
    list_display_links = ('name',)
    list_filter = ('archive_format',)
    ordering = ('archive_format', 'name')
    search_fields = ('name',)


class TestCaseAdmin(admin.ModelAdmin):
    """The admin site configuration for the TestCase model."""
    fields = ('name',)
    list_display = ('name',)
    list_display_links = ('name',)
    ordering = ('name',)
    search_fields = ('name',)


class BugExResultAdmin(admin.ModelAdmin):
    """The admin configuration for the BugExResult model."""
    list_display = ('date',)
    list_display_links = ('date',)
    ordering = ('date',)
    search_fields = ('date',)


class FactAdmin(admin.ModelAdmin):
    """The admin configuration for the Fact model."""
    fieldsets = (
        (None, {
            'fields': ('class_name', 'method_name', 'line_number')
        }),
        (None, {
            'fields': ('bugex_result', 'fact_type')
        }),
        (None, {
            'fields': ('explanation',)
        })
    )
    list_display = ('class_name', 'method_name', 'line_number',
                    'bugex_result', 'fact_type', 'explanation')
    list_display_links = ('class_name',)
    list_filter = ('class_name', 'fact_type')
    ordering = ('class_name', 'bugex_result')
    search_fields = ('class_name', 'method_name', 'explanation')


admin.site.register(UserRequest, UserRequestAdmin)
admin.site.register(CodeArchive, CodeArchiveAdmin)
admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(BugExResult, BugExResultAdmin)
admin.site.register(Fact, FactAdmin)
admin.site.register(Folder)
admin.site.register(SourceFile)
admin.site.register(ClassFile)
admin.site.register(Line)
admin.site.register(MethodElement)
admin.site.register(FieldElement)
admin.site.register(ClassElement)
