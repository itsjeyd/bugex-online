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


admin.site.register(UserRequest, UserRequestAdmin)
admin.site.register(CodeArchive)
admin.site.register(TestCase)
admin.site.register(BugExResult)
admin.site.register(Fact)
admin.site.register(Folder)
admin.site.register(SourceFile)
admin.site.register(ClassFile)
admin.site.register(Line)
admin.site.register(MethodElement)
admin.site.register(FieldElement)
admin.site.register(ClassElement)
