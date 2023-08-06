import subprocess

from django.conf import settings
from django.core.management.base import BaseCommand
import os


class Command(BaseCommand):
    can_import_settings = True

    def add_arguments(self, parser):
        parser.add_argument('action', nargs='?')
        parser.add_argument('--local', action='store_true')

    def install(self, local):
        if local:
            subprocess.call(
                ['npm', 'install'], cwd='{0}/website/static'.format(settings.BASE_DIR)
            )
            return

        for package in open(os.path.join(settings.PROJECT_DIR, 'requirements', 'npm.txt')):
            subprocess.call(
                ['sudo', 'npm', 'install', '-g', package])

    def handle(self, *args, **options):
        if options['action'] != 'install':
            return

        print("Installing NPM dependencies")

        self.install(options['local'])
        return
