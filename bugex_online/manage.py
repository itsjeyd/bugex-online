# -*- coding: utf-8 -*-
#!/usr/bin/env python

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

import os
import sys

if __name__ == "__main__":
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bugex_online.settings")

    from django.core.management import execute_from_command_line

    execute_from_command_line(sys.argv)
