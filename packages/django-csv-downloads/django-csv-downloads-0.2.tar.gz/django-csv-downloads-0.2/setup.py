# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['django_csv', 'django_csv.migrations']

package_data = \
{'': ['*']}

install_requires = \
['django>=2.2,<4.0']

setup_kwargs = {
    'name': 'django-csv-downloads',
    'version': '0.2',
    'description': 'Django app for enabling and tracking CSV downloads',
    'long_description': '# Django CSV Downloads\n\nDjango app for tracking queryset-backed CSV downloads\n\n### Version support\n\nThe current version of the this app support **Python 3.8+** and **Django 2.2+**\n\n## What does this app do?\n\nThis app is used to track user downloads of CSVs that are derived from Django QuerySets. You provide\nthe filename, queryset and the list of columns that you want to output.\n\nIt has a single model (`CsvDownload`) that tracks downloads and stores the user, filename, row count\nand timestamp.\n\n## Usage\n\nThe recommended way to use this app is to rely on `django_csv.views.download_csv`, which wraps up\nthe creation of the download object and the generation of the CSV itself:\n\n```python\n# DISPLAY PURPOSES ONLY: DO NOT ENABLE USER DATA DOWNLOADS IN PRODUCTION\ndef download_users(request: HttpRequest) -> HttpResponse:\n    data = User.objects.all()\n    columns = ("first_name", "last_name", "email")\n    return download_csv(request.user, "users.csv", data, *columns)\n```\n\n## Settings\n\nThere is a `CSV_DOWNLOAD_MAX_ROWS` setting that is used to truncate output. Defaults to 10000.\n\n## Examples\n\n**Caution:** All of these examples involve the User model as it\'s ubiquitous - DO NOT DO THIS ON A\nPRODUCTION ENVIRONMENT.\n\nExample of writing a QuerySet to a file:\n\n```python\n>>> data = User.objects.all()\n>>> columns = ("first_name", "last_name", "email")\n>>> with open(\'users.csv\', \'w\') as csvfile:\n>>>     csv.write_csv(csvfile, data, *columns)\n10  #<--- row count\n```\n\nExample of writing to an HttpResponse:\n\n```python\n>>> response = HttpResponse(content_type="text/csv")\n>>> response["Content-Disposition"] = \'attachment; filename="users.csv"\'\n>>> csv.write_csv(response, data, *columns)\n10\n```\n\nExample of writing to an in-memory text buffer:\n\n```python\n>>> buffer = io.StringIO()\n>>> csv.write_csv(buffer, data, *columns)\n10\n```\n\nExample of a custom admin action to download User data:\n\n```python\nclass CustomUserAdmin(UserAdmin):\n\n    actions = [\'download\']\n    csv_fields = ("first_name", "last_name", "email", "is_staff")\n    csv_filename = "users.csv"\n\n    def download(self, request, queryset):\n        """Download selected users as a CSV."""\n        return download_csv(\n            user=request.user,\n            filename=CustomUserAdmin.csv_filename,\n            queryset=queryset,\n            *CustomUserAdmin.csv_fields\n        )\n\n    download.short_description = "Download selected users"\n```\n\nExample CBV\n\n```python\nclass UserDownloadView(CsvDownloadView):\n    """Staff-only user downloads view."""\n\n    def is_permitted(self, request):\n        return request.user.is_staff\n\n    def filename(self, request):\n        return "users.csv"\n\n    def columns(self, request):\n        return ("first_name", "last_name", "email")\n\n    def queryset(self, request):\n        return User.objects.all()\n```\n',
    'author': 'YunoJuno',
    'author_email': 'code@yunojuno.com',
    'maintainer': 'YunoJuno',
    'maintainer_email': 'code@yunojuno.com',
    'url': 'https://github.com/yunojuno/django-csv-downloads',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'python_requires': '>=3.8,<4.0',
}


setup(**setup_kwargs)
