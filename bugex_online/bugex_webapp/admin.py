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


class FolderAdmin(admin.ModelAdmin):
    """The admin configuration for the Folder model."""
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (None, {
            'fields': ('code_archive',)
        }),
        ('Optional', {
            'fields': ('parent_folder',)
        })
    )
    list_display = ('name', 'code_archive', 'parent_folder')
    list_display_links = ('name',)
    list_filter = ('code_archive',)
    ordering = ('code_archive', 'name')
    search_fields = ('name',)


class SourceFileAdmin(admin.ModelAdmin):
    """The admin configuration for the SourceFile model."""
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (None, {
            'fields': ('code_archive', 'folder')
        }),
        ('Optional', {
            'fields': ('package',)
        })
    )
    list_display = ('name', 'code_archive', 'folder', 'package')
    list_display_links = ('name',)
    ordering = ('code_archive', 'name')
    search_fields = ('name', 'code_archive', 'folder')


class ClassFileAdmin(admin.ModelAdmin):
    """The admin configuration for the ClassFile model."""
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (None, {
            'fields': ('code_archive', 'folder')
        })
    )
    list_display = ('name', 'code_archive', 'folder')
    list_display_links = ('name',)
    ordering = ('code_archive', 'name')
    search_fields = ('name', 'code_archive', 'folder')


class LineAdmin(admin.ModelAdmin):
    """The admin configuration for the Line model."""
    fieldsets = (
        (None, {
            'fields': ('content', 'number')
        }),
        (None, {
            'fields': ('source_file',)
        }),
        (None, {
            'fields': ('definition',)
        })
    )
    list_display = ('content', 'number', 'source_file', 'definition')
    list_display_links = ('content',)
    list_filter = ('definition',)
    ordering = ('source_file', 'number')
    search_fields = ('content', 'number', 'source_file')


class MethodElementAdmin(admin.ModelAdmin):
    """The admin configuration for the MethodElement model."""
    fieldsets = (
        (None, {
            'fields': ('name', 'arguments', 'return_type')
        }),
        (None, {
            'fields': ('access_level', 'class_element', 'line')
        }),
        ('Optional', {
            'fields': ('comment',)
        })
    )
    list_display = ('name', 'arguments', 'return_type',
                    'access_level', 'class_element', 'line', 'comment')
    list_display_links = ('name',)
    list_filter = ('access_level',)
    ordering = ('name',)
    search_fields = ('name', 'arguments', 'return_types', 'class_element',
                     'comment')


class FieldElementAdmin(admin.ModelAdmin):
    """The admin configuration for the FieldElement model."""
    fieldsets = (
        (None, {
            'fields': ('name', 'field_type')
        }),
        (None, {
            'fields': ('access_level', 'class_element', 'line')
        }),
        ('Optional', {
            'fields': ('comment',)
        })
    )
    list_display = ('name', 'field_type', 'access_level',
                    'class_element', 'line', 'comment')
    list_display_links = ('name',)
    list_filter = ('access_level',)
    ordering = ('name',)
    search_fields = ('name', 'field_type', 'class_element', 'comment')


class ClassElementAdmin(admin.ModelAdmin):
    """The admin configuration for the ClassElement model."""
    fieldsets = (
        (None, {
            'fields': ('name',)
        }),
        (None, {
            'fields': ('access_level', 'line')
        }),
        ('Optional', {
            'fields': ('class_element', 'comment')
        })
    )
    list_display = ('name', 'access_level', 'class_element', 'line', 'comment')
    list_display_links = ('name',)
    list_filter = ('access_level',)
    ordering = ('name',)
    search_fields = ('name', 'class_element', 'comment')


admin.site.register(UserRequest, UserRequestAdmin)
admin.site.register(CodeArchive, CodeArchiveAdmin)
admin.site.register(TestCase, TestCaseAdmin)
admin.site.register(BugExResult, BugExResultAdmin)
admin.site.register(Fact, FactAdmin)
admin.site.register(Folder, FolderAdmin)
admin.site.register(SourceFile, SourceFileAdmin)
admin.site.register(ClassFile, ClassFileAdmin)
admin.site.register(Line, LineAdmin)
admin.site.register(MethodElement, MethodElementAdmin)
admin.site.register(FieldElement, FieldElementAdmin)
admin.site.register(ClassElement, ClassElementAdmin)
