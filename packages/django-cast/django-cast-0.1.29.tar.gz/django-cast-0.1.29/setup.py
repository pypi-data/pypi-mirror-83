# -*- coding: utf-8 -*-
from setuptools import setup

modules = \
['commands']
install_requires = \
['Pillow>=7,<8',
 'coreapi>=2.3.3,<3.0.0',
 'django-allauth>=0.42,<0.43',
 'django-ckeditor>=6,<7',
 'django-environ>=0.4.5,<0.5.0',
 'django-filepond>=0.1.2,<0.2.0',
 'django-filter>=2.2.0,<3.0.0',
 'django-imagekit>=4.0.2,<5.0.0',
 'django-model-utils>=4.0.0,<5.0.0',
 'django-threadedcomments>=1.2,<2.0',
 'django-watson>=1.5.4,<2.0.0',
 'django>=3.1,<4.0',
 'djangorestframework>=3.11.0,<4.0.0',
 'feedparser>=6,<7',
 'markdown>=3.2.1,<4.0.0',
 'plotly>=4.5.2,<5.0.0',
 'python-slugify>=4.0.0,<5.0.0',
 'wagtail>=2.8,<3.0',
 'wagtail_srcset>=0.1,<0.2']

entry_points = \
{'console_scripts': ['autoformat = commands:black',
                     'clean = commands:clean',
                     'clean-build = commands:clean_build',
                     'clean-pyc = commands:clean_pyc',
                     'docs = commands:docs',
                     'lint = commands:flake8',
                     'notebook = commands:notebook',
                     'show_coverage = commands:coverage',
                     'test = commands:test']}

setup_kwargs = {
    'name': 'django-cast',
    'version': '0.1.29',
    'description': 'Just another blogging / podcasting package',
    'long_description': '',
    'author': 'Jochen Wersdörfer',
    'author_email': 'jochen@wersdoerfer.de',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/ephes/django-cast',
    'py_modules': modules,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.9,<4.0',
}


setup(**setup_kwargs)
