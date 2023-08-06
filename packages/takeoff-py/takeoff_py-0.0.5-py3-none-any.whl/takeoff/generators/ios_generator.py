from .generator_base import GeneratorBase

class IosGenerator(GeneratorBase):
    def __init__(self, name, subtype, options):
        self.name = name
        self.subtype = subtype

    def run(self):
        self.setup()
        print(f"Running iOS Project Generator: {self.name}")