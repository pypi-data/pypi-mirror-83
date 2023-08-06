import os
from jinja2 import Template
from .generator_base import GeneratorBase

class AndroidGenerator(GeneratorBase):

    def __init__(self, name, subtype, options):
        self.name = name
        self.subtype = subtype
        self.options = options
        self.android_prefix = ''

        for option in options:
            if 'android_prefix' in option:
                self.android_prefix = option.split('=')[1]        

        self.product_package = f"{self.android_prefix}.{self.name.replace(' ', '').lower()}"

    def run(self):
        self.setup()
        print(f">>> Running Android Project Generator: {self.name}")
        self.create_structure_folders()
        self.create_structure_files()

    
    def product_path(self):
        return f"{self.android_prefix.replace('.', '/')}/{self.name.replace(' ', '').lower()}"

    def create_structure_folders(self):
        print(f">>> Creating directory structure: {self.android_prefix}.{self.name}")

        for folder in self.main_project_folders():
            fullpath = f"dist/{self.name.replace(' ', '').lower()}/android/{folder}"
            print(f"    Creating Android Folder: {fullpath}")
            os.system(f"mkdir -p {fullpath}")

    def create_structure_files(self):
        print(f">>> Creating file structure: {self.android_prefix}.{self.name}")

        main_files = self.main_project_files()
        for template_source in main_files:
            destination = f"dist/{self.name.replace(' ', '').lower()}/android/{main_files[template_source]}"
            print(f"    Creating Android File: {destination}")
            self.render_template_file(template_source, destination)

    def render_template_file(self, template_source, destination):
        template_path = os.path.join(BASE_DIR, f"templates/android/{template_source}.template")
        
        with open(template_path) as f:
            template_contents = f.read()

        template = Template(template_contents)
        with open(destination, 'w') as f:
            f.write(template.render())

    def main_project_folders(self):
        return [
            '',
            'app',
            'app/src',
            'app/src/androidTest',
            'app/src/androidTest/java',
            "app/src/androidTest/java/#{product_path}",
            'app/src/main',
            'app/src/main/java',
            f"app/src/main/java/#{self.android_prefix.replace('.', '/')}",
            f"app/src/main/java/{self.product_path()}",
            f"app/src/main/java/{self.product_path()}/main",
            f"app/src/main/java/{self.product_path()}/model",
            f"app/src/main/java/{self.product_path()}/fragments",
            f"app/src/main/java/{self.product_path()}/activities",
            f"app/src/main/java/{self.product_path()}/service/model",
            f"app/src/main/java/{self.product_path()}/ui",
            f"app/src/main/java/{self.product_path()}/ui/main",
            'app/src/main/res',
            'app/src/main/res/menu',
            'app/src/main/res/animator',
            'app/src/main/res/drawable',
            'app/src/main/res/drawable-v24',
            'app/src/main/res/layout',
            'app/src/main/res/xml',
            'app/src/main/res/mipmap-anydpi-v26',
            'app/src/main/res/mipmap-hdpi',
            'app/src/main/res/mipmap-mdpi',
            'app/src/main/res/mipmap-xhdpi',
            'app/src/main/res/mipmap-xxhdpi',
            'app/src/main/res/mipmap-xxxhdpi',
            'app/src/main/res/values',
            'app/src/test',
            'app/src/test/java',
            'app/src/test/java/com',
            f"app/src/test/java/#{self.android_prefix.replace('.', '/')}",
            f"app/src/test/java/{self.product_path()}",
            '.idea',
            '.idea/codeStyles',
            'gradle/wrapper'
        ]
    
    def main_project_files(self):
        return {
            '.gitignore': '.gitignore',
            'local.properties': 'local.properties',
            'Project.iml': "#{@product.name.gsub(' ', '')}.iml",
            'Project.xml': '.idea/codeStyles/Project.xml',
            'codeStyleConfig.xml': '.idea/codeStyles/codeStyleConfig.xml',
            'idea_gradle.xml': '.idea/gradle.xml',
            'misc.xml': '.idea/misc.xml',
            'runConfigurations.xml': '.idea/runConfigurations.xml',
            'build.gradle': 'build.gradle',
            'gradle.properties': 'gradle.properties',
            'gradle-wrapper.properties': 'gradle/wrapper/gradle-wrapper.properties',
            'gradlew': 'gradlew',
            'gradlew.bat': 'gradlew.bat',
            'settings.gradle': 'settings.gradle',
            'google-services.json': 'app/google-services.json',
            'app_gitignore': 'app/.gitignore',
            'app_build.gradle': 'app/build.gradle',
            'proguard-rules.pro': 'app/proguard-rules.pro',
            'ExampleInstrumentedTest.kt': f"app/src/androidTest/java/{self.product_path()}/ExampleInstrumentedTest.kt",
            'AndroidManifest.xml': 'app/src/main/AndroidManifest.xml',
            'BaseFragment.kt': f"app/src/main/java/{self.product_path()}/main/BaseFragment.kt",
            'BaseDialogFragment.kt': f"app/src/main/java/{self.product_path()}/main/BaseDialogFragment.kt",
            'BaseActivity.kt': f"app/src/main/java/{self.product_path()}/main/BaseActivity.kt",
            'network_security_config.xml': 'app/src/main/res/xml/network_security_config.xml',
            'file_paths.xml': 'app/src/main/res/xml/file_paths.xml',
            'toolbar_elevation.xml': 'app/src/main/res/animator/toolbar_elevation.xml',
            'ic_launcher_foreground.xml': 'app/src/main/res/drawable-v24/ic_launcher_foreground.xml',
            'ic_launcher_background.xml': 'app/src/main/res/drawable/ic_launcher_background.xml',
            'ic_launcher.xml': 'app/src/main/res/mipmap-anydpi-v26/ic_launcher.xml',
            'ic_launcher_round.xml': 'app/src/main/res/mipmap-anydpi-v26/ic_launcher_round.xml',
            'border_rounded_gray.xml': 'app/src/main/res/drawable/border_rounded_gray.xml',
            'button_background.xml': 'app/src/main/res/drawable/button_background.xml',
            'button_white_background.xml': 'app/src/main/res/drawable/button_white_background.xml',
            'link_button.xml': 'app/src/main/res/drawable/link_button.xml',
            'google_button_background.xml': 'app/src/main/res/drawable/google_button_background.xml',
            'facebook_button_background.xml': 'app/src/main/res/drawable/facebook_button_background.xml',
            'ic_notifications_black_24dp.xml': 'app/src/main/res/drawable/ic_notifications_black_24dp.xml',
            'v24_ic_notifications_black_24dp.xml': 'app/src/main/res/drawable-v24/ic_notifications_black_24dp.xml',
            'data_table_view_cell.xml': 'app/src/main/res/layout/data_table_view_cell.xml',
            'colors.xml': 'app/src/main/res/values/colors.xml',
            'strings.xml': 'app/src/main/res/values/strings.xml',
            'styles.xml': 'app/src/main/res/values/styles.xml',
            'ExampleUnitTest.kt': f"app/src/test/java/{self.product_path()}/ExampleUnitTest.kt",
            'RestEntity.kt': f"app/src/main/java/{self.product_path()}/model/RestEntity.kt",
            'ApiController.kt': f"app/src/main/java/{self.product_path()}/service/ApiController.kt",
            'BadgeUtils.kt': f"app/src/main/java/{self.product_path()}/service/BadgeUtils.kt",
            'CableHelper.kt': f"app/src/main/java/{self.product_path()}/service/CableHelper.kt",
            'CableInterface.kt': f"app/src/main/java/{self.product_path()}/service/CableInterface.kt",
            'DelegateError.kt': f"app/src/main/java/{self.product_path()}/service/DelegateError.kt",
            'FirebaseMessaging.kt': f"app/src/main/java/{self.product_path()}/service/FirebaseMessaging.kt",
            'LoginService.kt': f"app/src/main/java/{self.product_path()}/service/LoginService.kt",
            'LoginServiceDelegate.kt': f"app/src/main/java/{self.product_path()}/service/LoginServiceDelegate.kt",
            'RestEntityService.kt': f"app/src/main/java/{self.product_path()}/service/RestEntityService.kt",
            'RestEntityServiceDelegate.kt': f"app/src/main/java/{self.product_path()}/service/RestEntityServiceDelegate.kt",
            'RubyThreeApiConnector.kt': f"app/src/main/java/{self.product_path()}/service/RubyThreeApiConnector.kt",
            'ServiceInterface.kt': f"app/src/main/java/{self.product_path()}/service/ServiceInterface.kt",
            'UploadServiceDelegate.kt': f"app/src/main/java/{self.product_path()}/service/UploadServiceDelegate.kt",
            'VolleyMultipartRequest.kt': f"app/src/main/java/{self.product_path()}/service/VolleyMultipartRequest.kt",
            'VolleyService.kt': f"app/src/main/java/{self.product_path()}/service/VolleyService.kt"
        }