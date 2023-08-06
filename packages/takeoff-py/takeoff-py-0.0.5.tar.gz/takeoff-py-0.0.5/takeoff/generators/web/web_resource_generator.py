import os
from jinja2 import Template
from .web_base_generator import WebBaseGenerator
from pathlib import Path

class WebResourceGenerator(WebBaseGenerator):
    def __init__(self, name, options):
        super().__init__(name, options)
        self.model_name = ''
        self.model_attributes = []

    def model_class_name(self):
        return self.camelize(self.model_name)

    def run(self):
        self.model_name = self.options.pop(0)
        print(f"Running Web Resource Generator: {self.name} : {self.model_name}")

        self.generate_layout()
        self.generate_nav_item()
        self.generate_root()
        self.load_model_attributes()
        self.write_view_file()
        self.update_views_file()
        self.write_form_file()
        self.write_views()
        self.prepare_urls()

    def generate_nav_item(self):
        self.generate_nav()
        
        shared = f"{self.project_folder()}/main/templates/shared"
        destination = f"{shared}/_nav.html"
        lines = list(open(destination, 'r'))
        last_line = self.resources_last_line(lines)

        url = "{% url 'main:" + self.pluralize(self.model_name) + "' %}"
        new_line = f"          <a class='dropdown-item' href='{url}'>{self.titleize(self.pluralize(self.model_name))}</a>\n"
        if new_line not in lines:
            lines.insert(last_line, new_line)
            last_line += 1

        with open(destination, 'w') as file:
            file.writelines(lines)        


    def writeable_attributes(self):
        atts = []
        locked_fields = ['created_at', 'updated_at']

        for attribute in self.model_attributes:
            if attribute['attribute_name'] not in locked_fields:
                atts.append(attribute)

        return atts

    def load_model_attributes(self):
        model_file = f"{self.project_folder()}/main/models/{self.model_name}.py"
        lines = list(open(model_file, 'r'))

        django_field_types = [
            'models.CharField',
            'models.TextField',
            'models.DateTimeField',
            'models.IntegerField',
            'models.BooleanField',
            'models.FloatField',
            'models.ForeignKey',
        ]

        for line in lines:
            for field_type in django_field_types:
                if f"= {field_type}" in line:
                    attribute_name = line.strip().split("=")[0].strip()
                    attribute_type = line.strip().split("=")[1].strip().split("(")[0].strip()
                    self.model_attributes.append({ 'attribute_name': attribute_name, 'attribute_type': attribute_type })

    def write_view_file(self):
        template_path = f"{self.templates_path}/web/view.template"
        destination_folder = f"{self.project_folder()}/main/views"
        os.system(f"mkdir -p {destination_folder}")
        Path(f"{destination_folder}/__init__.py").touch()
        destination = f"{destination_folder}/{self.pluralize(self.model_name)}.py"

        with open(template_path) as f:
            template_contents = f.read()

        template = Template(template_contents)
        contents = template.render(generator=self)

        with open(destination, 'w') as f:
            f.write(contents)

    def write_form_file(self):
        template_path = f"{self.templates_path}/web/form.template"
        destination_folder = f"{self.project_folder()}/main/forms"
        os.system(f"mkdir -p {destination_folder}")
        destination = f"{destination_folder}/{self.model_name}.py"

        with open(template_path) as f:
            template_contents = f.read()

        template = Template(template_contents)
        contents = template.render(generator=self)

        with open(destination, 'w') as f:
            f.write(contents)

    def update_views_file(self):
        current_file = f"{self.project_folder()}/main/views/__init__.py"
        lines = list(open(current_file, 'r'))
        line = f"from .{self.pluralize(self.model_name)} import *\n"
        if line not in lines:
            lines.append(line)
        
        with open(current_file, 'w') as file:
            file.writelines(lines)
    
    def write_views(self):
        views = ['index', 'show', 'new', 'edit']
        for view in views:
            self.render_view_template(view)

    def render_view_template(self, view):
        template_path = f"{self.templates_path}/web/views/{view}.html.template"
        destination_folder = f"{self.project_folder()}/main/templates/{self.pluralize(self.model_name)}"
        os.system(f"mkdir -p {destination_folder}")
        destination = f"{destination_folder}/{view}.html"
        self.render_template(template_path, destination)

    def prepare_urls(self):
        urls_file = f"dist/{self.name}/web/{self.name}/main/urls.py"
        file = open(urls_file, 'r')
        lines = list(file)
        file.close()

        for index, line in enumerate(lines):
            if line == "from django.urls import path\n":
                lines[index] = line.replace('path', 'path, include')

        new_paths = [
            [f"{self.pluralize(self.model_name)}/", f"views.{self.pluralize(self.model_name)}.index", self.pluralize(self.model_name)],
            [f"{self.pluralize(self.model_name)}/new", f"views.{self.pluralize(self.model_name)}.new", f"new_{self.model_name}"],
            [f"{self.pluralize(self.model_name)}/<int:{self.model_name}_id>", f"views.{self.pluralize(self.model_name)}.show", self.model_name],
            [f"{self.pluralize(self.model_name)}/<int:{self.model_name}_id>/edit", f"views.{self.pluralize(self.model_name)}.edit", f"edit_{self.model_name}"],
            [f"{self.pluralize(self.model_name)}/<int:{self.model_name}_id>/delete", f"views.{self.pluralize(self.model_name)}.delete", f"delete_{self.model_name}"]
        ]

        for new_path in new_paths:
            self.add_main_url_pattern(new_path[0], new_path[1], new_path[2])

    def urls_last_line(self, lines):
        started = False
        finish = 0

        for index, line in enumerate(lines):
            if 'urlpatterns' in line:
                started = True
            if started and finish == 0 and ']' in line:
                finish = index

        return finish
    
    def fields_list(self):
        fields = list(map(lambda x: f"'{x['attribute_name']}'", self.writeable_attributes()))
        fields = ", ".join(fields)
        return f"[{fields}]"
    
    def labels_list(self):
        fields = list(map(lambda x: f"'{x['attribute_name']}': '{self.titleize(x['attribute_name'])}'", self.writeable_attributes()))
        fields = ", ".join(fields)
        return '{' + f"{fields}" + '}'