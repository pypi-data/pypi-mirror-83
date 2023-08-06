# coding=utf-8

from subprocess import call

from .template import Template, ProjectInfo
from .pb import pasteboard_read
from .command import Command, CommandOption
from .encoder import Encoder
from .model import Model, Enum


class TemplateCommand(Command):
    def __init__(self, template_name, scene_name, options):
        super(TemplateCommand, self).__init__()
        self.template_name = template_name
        self.scene_name = scene_name
        self.options = CommandOption(options)

    def get_project_package_name(self):
        try:
            infile = open('pubspec.yaml', 'r')
            return infile.readline().replace('name:','').strip()
        except (IOError, OSError) as e:
            print("Please run this command in flutter folder.")
            exit(1)

    def create_files(self):
        if self.template_name == Template.TemplateType.BASE:
            template = Template.BaseTemplate(
                self.options,
                self.scene_name,
                self.get_project_package_name()
            )
            output_path = template.create_files()
        else:
            print("Invalid template type.")
            exit(1)
