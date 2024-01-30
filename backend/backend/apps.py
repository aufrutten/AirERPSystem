from pathlib import Path


def import_apps():
    """importing all apps in folder which have the apps.py with configuration of app"""
    apps = []
    apps_folder = Path(__file__).parents[1] / 'apps'  # /AirERPSystem/backend/apps/
    for app_name in apps_folder.iterdir():  # app_name = 'accounts'
        app_path = apps_folder / app_name  # /AirERPSystem/backend/apps/accounts/
        if app_path.is_dir() and (app_path / 'apps.py').exists():
            apps.append(f'{apps_folder.name}.{app_name.name}')
    return apps


if __name__ == '__main__':
    print(import_apps())
