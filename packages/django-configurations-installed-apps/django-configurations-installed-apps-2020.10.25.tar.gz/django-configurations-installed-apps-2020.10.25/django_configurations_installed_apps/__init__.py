import os

from configurations import Configuration, values
import django_discover_apps


def getlines(path):
    if not path:
        return []
    return list(filter(None, open(path).read().splitlines()))


class InstalledAppsMixin:
    INSTALLED_APPS_FILE = values.Value(None)
    INSTALLED_APPS_FILES = values.ListValue([])
    INSTALLED_APPS_DISCOVER = values.Value(True)

    @classmethod
    def setup(cls):
        super(InstalledAppsMixin, cls).setup()
        f_list = cls.INSTALLED_APPS_FILES or [cls.INSTALLED_APPS_FILE]
        for f in filter(None, f_list):
            for l in getlines(f):
                if l.strip() and l.strip() not in cls.MIDDLEWARE:
                    cls.INSTALLED_APPS.append(l.strip())
        if cls.INSTALLED_APPS_DISCOVER:
            path = cls.BASE_DIR if hasattr(cls, 'BASE_DIR') else os.getcwd()
            for app in django_discover_apps.discover_apps(path):
                if app not in cls.INSTALLED_APPS:
                    cls.INSTALLED_APPS.append(app)


class InstalledAppsConfiguration(InstalledAppsMixin, Configuration):
    pass
