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

from bugex_webapp.models import SourceFile, ClassFile, Line, \
    MethodElement, FieldElement, ClassElement, Folder, BugExResult

admin.site.register(SourceFile)
admin.site.register(ClassFile)
admin.site.register(Line)
admin.site.register(MethodElement)
admin.site.register(FieldElement)
admin.site.register(ClassElement)
admin.site.register(Folder)
admin.site.register(BugExResult)