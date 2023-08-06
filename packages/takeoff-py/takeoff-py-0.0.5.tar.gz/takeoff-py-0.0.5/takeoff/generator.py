from jinja2 import Template
from .generators import *

class Generator:
    def __init__(self, arguments):
        self.generator_subtype = ''
        self.generator_type = ''

        if len(arguments) < 2:
            self.print_instructions()
        else:
            generator = arguments.pop(0)
            self.set_generator_type(generator)
            self.name = arguments.pop(0)
            self.options = arguments

    def print_instructions(self):
        print('This package helps with your project takeoff by creating views, models and project structure based off of JSON files')
    
    def set_generator_type(self, generator):
        parts = [generator]

        if ':' in generator:
            parts = generator.split(':')

        self.generator_type = parts[0]
        if len(parts) > 1:
            self.generator_subtype = parts[1]

    def run(self):
        generator = self.get_generator()
        generator.run()
    
    def get_generator(self):
        klass_name = ''.join(x for x in f"{self.generator_type.replace('_', ' ')} Generator".title() if not x.isspace())
        return eval(f"{klass_name}(self.name, self.generator_subtype, self.options)")