import os
from jinja2 import Template
from .web_base_generator import WebBaseGenerator
from pathlib import Path

class WebModelGenerator(WebBaseGenerator):
    def __init__(self, name, options):
        super().__init__(name, options)
        self.model_name = ''
        self.model_attributes = []
        self.associations = []

    def model_class_name(self):
        return self.camelize(self.model_name)

    def run(self):
        self.model_name = self.options.pop(0)
        print(f"Running Web Model Generator: {self.name} : {self.model_name}")

        for attribute in self.options:
            parts = attribute.split(':')
            if len(parts) == 1:
                parts.append('string')

            self.model_attributes.append({
                'name': parts[0], 
                'type': parts[1], 
                'class': self.attribute_class(parts[1]),
                'field_extra': self.attribute_field_extra(parts[1], self.camelize(parts[0]))
            })

            if parts[1] == 'belongs_to':
                self.associations.append({
                    'name': parts[0], 
                    'class_name': self.camelize(parts[0])
                })
        
        self.model_attributes.append({
            'name': 'created_at',
            'type': 'datetime',
            'class': 'DateTimeField',
            'field_extra': 'auto_now_add=True'
        })

        self.model_attributes.append({
            'name': 'updated_at',
            'type': 'datetime',
            'class': 'DateTimeField',
            'field_extra': 'auto_now_add=True'
        })        

        self.write_model_file()
        self.update_models_file()        
        self.generate_migration()
        self.register_admin()
    
    def attribute_class(self, type):
        switcher = { 
            'string': 'CharField', 
            'text': 'TextField', 
            'integer': 'IntegerField',
            'float': 'FloatField',
            'boolean': 'BooleanField',            
            'belongs_to': 'ForeignKey',
        }
        return switcher.get(type, 'CharField')
    
    def attribute_field_extra(self, type, association_class = ''):
        switcher = { 
            'string': "default='', max_length=250", 
            'integer': 'default=0',
            'float': 'default=0.0',
            'text': "default=''",
            'boolean': 'default=False',
            'belongs_to': f"{association_class}, on_delete=models.CASCADE,  null=True"
        }   
        return switcher.get(type, "default='', max_length=250")

    def write_model_file(self):
        template_path = f"{self.templates_path}/web/model.template"
        destination_folder = f"{self.project_folder()}/main/models"
        os.system(f"mkdir -p {destination_folder}")
        Path(f"{destination_folder}/__init__.py").touch()
        destination = f"{destination_folder}/{self.model_name}.py"

        with open(template_path) as f:
            template_contents = f.read()

        template = Template(template_contents)
        contents = template.render(generator=self)
        
        with open(destination, 'w') as f:
            f.write(contents)

    def update_models_file(self):
        current_file = f"{self.project_folder()}/main/models/__init__.py"

        lines = list(open(current_file, 'r'))
        lines.append(f"from .{self.model_name} import {self.model_class_name()}\n")
        
        with open(current_file, 'w') as file:
            file.writelines(lines)

    def models_last_line(self, lines):
        return len(lines)
    
    def generate_migration(self):
        os.system(f"cd {self.project_folder()} && {self.python} manage.py makemigrations")
    
    def register_admin(self):
        current_file = f"{self.project_folder()}/main/admin.py"
        import_line = f"from .models.{self.model_name} import {self.model_class_name()}\n"
        register_line = f"admin.site.register({self.model_class_name()})\n"
        
        last_import_line_index = 0
        lines = list(open(current_file, 'r'))

        if import_line in lines or register_line in lines:
            return

        for index, line in enumerate(lines):
            if 'import' not in line:
                last_import_line_index = index
        
        lines.insert(last_import_line_index, import_line)
        lines.append(register_line)

        with open(current_file, 'w') as file:
            file.writelines(lines)        