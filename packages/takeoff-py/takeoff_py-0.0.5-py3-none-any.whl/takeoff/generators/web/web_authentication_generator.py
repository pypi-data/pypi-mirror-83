import os
from jinja2 import Template
from .web_base_generator import WebBaseGenerator
from pathlib import Path

class WebAuthenticationGenerator(WebBaseGenerator):
    def __init__(self, name, options):
        super().__init__(name, options)

    def run(self):
        print(f"Running Web Authentication Generator: {self.name}")
        self.generate_layout()
        self.generate_nav()
        self.generate_root()
        self.generate_users_app()        
        self.generate_auth_nav()
        self.add_app('users')
        self.add_app_url_pattern('users', 'users/')
        self.generate_auth_urls()
        self.generate_auth_view()
        self.generate_login_form()
        self.generate_registration_form()

    def generate_nav_auth_file(self):
        shared = f"{self.project_folder()}/main/templates/shared"
        os.system(f"mkdir -p {shared}")
        destination = f"{shared}/_nav_auth.html"
        template_path = f"{self.templates_path}/web/views/nav_auth.html.template"
        self.render_template(template_path, destination)

    def generate_auth_nav(self):
        nav_file = f"dist/{self.name}/web/{self.name}/main/templates/shared/_nav.html"
        lines = list(open(nav_file, 'r'))
        last_line = self.auth_last_line(lines)

        new_line = "    {% include 'shared/_nav_auth.html' %}\n"
        if new_line not in lines:
            lines.insert(last_line, new_line)
        
        with open(nav_file, 'w') as file:
            file.writelines(lines)
        
        self.generate_nav_auth_file()

    def generate_users_app(self):
        os.system(f"cd {self.project_folder()} && {self.python} manage.py startapp users")

    def generate_auth_urls(self):
        destination = f"{self.project_folder()}/users/urls.py"
        template_path = f"{self.templates_path}/web/auth_urls.template"
        self.render_template(template_path, destination)

    def generate_auth_view(self):
        destination = f"{self.project_folder()}/users/views.py"
        template_path = f"{self.templates_path}/web/auth_view.template"
        self.render_template(template_path, destination, True)

    def generate_login_form(self):
        registration = f"{self.project_folder()}/users/templates/registration"
        os.system(f"mkdir -p {registration}")
        destination = f"{registration}/login.html"
        template_path = f"{self.templates_path}/web/views/login_form.html.template"
        self.render_template(template_path, destination)

    def generate_registration_form(self):
        registration = f"{self.project_folder()}/users/templates/registration"
        os.system(f"mkdir -p {registration}")
        destination = f"{registration}/register.html"
        template_path = f"{self.templates_path}/web/views/registration_form.html.template"
        self.render_template(template_path, destination)