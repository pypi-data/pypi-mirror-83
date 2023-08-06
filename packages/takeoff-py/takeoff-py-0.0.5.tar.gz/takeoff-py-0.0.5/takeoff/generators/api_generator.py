from .generator_base import GeneratorBase

class ApiGenerator(GeneratorBase):
    def __init__(self, name, subtype, options):
        self.name = name
        self.subtype = subtype

    def run(self):
        self.setup()
        print(f"Running API Project Generator: {self.name}")