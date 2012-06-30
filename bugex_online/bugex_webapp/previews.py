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

This module contains form preview classes which are used to test all the
different forms for correct validation. For more information about form
previews, see:

https://docs.djangoproject.com/en/1.4/ref/contrib/formtools/form-preview/

"""

from django.contrib.formtools.preview import FormPreview
from django.http import HttpResponseRedirect

class BugExFormPreview(FormPreview):
    """The BugEx form preview class used for testing all forms of this project."""
    form_template = 'formtools/form.html'
    preview_template = 'formtools/preview.html'

    def done(self, request, cleaned_data):
        return HttpResponseRedirect('/main/')