import os
from jinja2 import Template
from ..generator_base import GeneratorBase
from pathlib import Path

class WebBaseGenerator(GeneratorBase):
    def __init__(self, name, options):
        super().__init__(name, options)

    def project_type(self):
        return 'web'

    def system_call(self, command):
        os.system(command)

    def render_template(self, template_path, destination, overwrite=False):
        if os.path.exists(destination) and not overwrite:
            return
        
        with open(template_path) as f:
            template_contents = f.read()

        template = Template(template_contents)
        contents = template.render(generator=self)
        with open(destination, 'w') as f:
            f.write(contents)

    def add_main_url_pattern(self, pattern, view_name, path_name):
        urls_file = f"{self.base_dist_folder()}/{self.name}/web/{self.name}/main/urls.py"
        file = open(urls_file, 'r')
        lines = list(file)
        file.close()

        for index, line in enumerate(lines):
            if line == "from django.urls import path\n":
                lines[index] = line.replace('path', 'path, include')

        last_line = self.urls_last_line(lines)
        new_line = f"    path('{pattern}', {view_name}, name='{path_name}'),\n"
        if new_line not in lines:
            lines.insert(last_line, new_line)

        with open(urls_file, 'w') as file:
            file.writelines(lines)

    def generate_layout(self):
        layouts = f"{self.project_folder()}/main/templates/layouts"
        os.system(f"mkdir -p {layouts}")
        destination = f"{layouts}/application.html"
        template_path = f"{self.templates_path}/web/views/layout.html.template"
        self.render_template(template_path, destination)

    def generate_root(self):
        main = f"{self.project_folder()}/main/templates/main"
        os.system(f"mkdir -p {main}")
        destination = f"{main}/index.html"
        template_path = f"{self.templates_path}/web/views/root.html.template"
        self.render_template(template_path, destination)
        self.render_main_view_template()
        self.add_main_url_pattern('', 'views.main.index', 'root')
    
        Path(f"{self.project_folder()}/main/views/__init__.py").touch()
        current_file = f"{self.project_folder()}/main/views/__init__.py"
        lines = list(open(current_file, 'r'))
        line = f"from .main import *\n"
        if line not in lines:
            lines.append(line)
        with open(current_file, 'w') as file:
            file.writelines(lines)            

    def generate_nav(self):
        shared = f"{self.project_folder()}/main/templates/shared"
        os.system(f"mkdir -p {shared}")
        destination = f"{shared}/_nav.html"
        template_path = f"{self.templates_path}/web/views/nav.html.template"
        self.render_template(template_path, destination)

    def urls_last_line(self, lines):
        started = False
        finish = 0

        for index, line in enumerate(lines):
            if 'urlpatterns' in line:
                started = True
            if started and finish == 0 and ']' in line:
                finish = index

        return finish

    def pattern_last_line(self, pattern, lines):
        finish = 0

        for index, line in enumerate(lines):
            if pattern in line:
                finish = index

        return finish

    def installed_apps_last_line(self, lines):
        started = False
        finish = 0

        for index, line in enumerate(lines):
            if 'INSTALLED_APPS' in line:
                started = True
            if started > 0 and finish == 0 and ']' in line:
                finish = index

        return finish

    def resources_last_line(self, lines):
        return self.pattern_last_line('EndResources', lines)

    def auth_last_line(self, lines):
        return self.pattern_last_line('EndAuth', lines)

    def render_main_view_template(self):
        template_path = f"{self.templates_path}/web/main_view.template"
        destination_folder = f"{self.project_folder()}/main/views/"
        os.system(f"mkdir -p {destination_folder}")
        destination = f"{destination_folder}/main.py"
        self.render_template(template_path, destination)

    def add_setting(self, setting, value):
        settings_file = f"{self.base_dist_folder()}/{self.name}/web/{self.name}/{self.name}/settings.py"
        file = open(settings_file, 'r')
        lines = list(file)
        file.close()
        last_line = len(lines)
        setting_line = f"{setting}='{value}'\n"

        if setting_line not in lines:
            lines.insert(last_line, setting_line)

        with open(settings_file, 'w') as file:
            file.writelines(lines)


    def add_app(self, app_name):
        settings_file = f"{self.base_dist_folder()}/{self.name}/web/{self.name}/{self.name}/settings.py"
        file = open(settings_file, 'r')
        lines = list(file)
        file.close()
        last_line = self.installed_apps_last_line(lines)
        lines.insert(last_line, f"    '{app_name}',\n")

        with open(settings_file, 'w') as file:
            file.writelines(lines)
    
    def add_app_url_pattern(self, app_name, pattern):
        urls_file = f"{self.base_dist_folder()}/{self.name}/web/{self.name}/{self.name}/urls.py"
        file = open(urls_file, 'r')
        lines = list(file)
        file.close()

        for index, line in enumerate(lines):
            if line == "from django.urls import path\n":
                lines[index] = line.replace('path', 'path, include')

        line = f"    path('{pattern}', include('{app_name}.urls')),\n"

        if line not in lines:
            last_line = self.urls_last_line(lines)
            lines.insert(last_line - 1, line)

        with open(urls_file, 'w') as file:
            file.writelines(lines)        