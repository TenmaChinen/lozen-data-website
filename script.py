import os
import shutil

# Set the path to your Django project directory
PROJECT_DIR = '.'

# Get a list of all the apps in the project
apps_dir = os.path.join(PROJECT_DIR, 'apps')
print(apps_dir)
# apps = [name for name in os.listdir(apps_dir) if os.path.isdir(os.path.join(apps_dir, name))]
