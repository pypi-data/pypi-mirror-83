import os
from jinja2 import Template
from .generator_base import GeneratorBase
from .web import *

class WebGenerator(GeneratorBase):
    def __init__(self, name, subtype, options):
        self.name = name
        self.subtype = subtype
        self.options = options

    def generator(self):
        klass_name = f"Web{self.subtype.replace('_', ' ').title()} Generator".replace(' ', '')
        return eval(f"{klass_name}(self.name, self.options)")

    def run(self):
        self.setup()
        self.generator().run()