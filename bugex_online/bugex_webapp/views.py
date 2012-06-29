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

from django.views.generic import TemplateView

class MainPageView(TemplateView):
    template_name = 'bugex_webapp/main.html'


class HowToPageView(TemplateView):
    template_name = 'bugex_webapp/howto.html'


class ResultsPageView(TemplateView):
    template_name = 'bugex_webapp/results.html'


class DeletePageView(TemplateView):
    template_name = 'bugex_webapp/delete.html'


class UserPageView(TemplateView):
    template_name = 'bugex_webapp/user.html'