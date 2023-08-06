# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['jekyllnb']

package_data = \
{'': ['*'], 'jekyllnb': ['templates/jekyll/*']}

install_requires = \
['nbconvert>=5.6.1,<7.0.0']

entry_points = \
{'console_scripts': ['jupyter-jekyllnb = '
                     'jekyllnb.jekyllnb:JekyllNB.launch_instance'],
 'nbconvert.exporters': ['jekyll = jekyllnb:JekyllExporter']}

setup_kwargs = {
    'name': 'jekyllnb',
    'version': '0.3.1',
    'description': 'Convert Jupyter Notebooks to Jekyll-ready Markdown files',
    'long_description': '# JekyllNB: Jupyter Notebooks to Jekyll Markdown\n\n[![Test Status](https://github.com/klane/jekyllnb/workflows/Tests/badge.svg)](https://github.com/klane/jekyllnb/actions)\n[![Documentation Status](https://img.shields.io/readthedocs/jekyllnb?label=Docs&logo=read%20the%20docs&logoColor=white)](https://jekyllnb.readthedocs.io/en/latest)\n[![Coverage Status](https://img.shields.io/codecov/c/github/klane/jekyllnb?label=Coverage&logo=codecov)](https://codecov.io/gh/klane/jekyllnb)\n[![LGTM](https://img.shields.io/lgtm/alerts/github/klane/jekyllnb?label=Alerts&logo=lgtm)](https://lgtm.com/projects/g/klane/jekyllnb/alerts)\n[![DeepSource](https://deepsource.io/gh/klane/jekyllnb.svg/?label=active+issues)](https://deepsource.io/gh/klane/jekyllnb/?ref=repository-badge)\n[![PyPI Version](https://img.shields.io/pypi/v/jekyllnb?color=blue&label=Version&logo=python&logoColor=white)](https://pypi.org/project/jekyllnb)\n[![Downloads](https://static.pepy.tech/personalized-badge/jekyllnb?period=total&units=international_system&left_color=grey&right_color=blue&left_text=Downloads)](https://pepy.tech/project/jekyllnb)\n[![License](https://img.shields.io/github/license/klane/jekyllnb?color=blue&label=License)](LICENSE)\n[![Code Style](https://img.shields.io/badge/Code%20Style-black-black)](https://github.com/psf/black)\n\nJekyllNB extends Jupyter\'s command line tool `nbconvert` to add the Jekyll front matter to Markdown files and save generated images to a desired location.\nThis allows you to easily convert all your notebooks to the required format and immediately build your Jekyll site.\nIt works great in a GitHub Actions workflow to convert your notebooks to Markdown and deploy to GitHub Pages.\nSee JekyllNB in action [here](https://github.com/klane/databall/blob/master/.github/workflows/gh-pages.yml).\n\n## Installation\n\nJekyllNB is available on PyPI and can be installed with `pip`.\n\n```bash\npip install jekyllnb\n```\n\n## Usage\n\nJekyllNB is a Jupyter app just like `nbconvert`. Call it with `jupyter jekyllnb`.\nThe preprocessor reads metadata from your notebook to populate the Jekyll front matter.\nAdd a `jekyll` section to your notebook metadata similar to:\n\n```json\n"jekyll": {\n    "layout": "notebook",\n    "permalink": "/hello/",\n    "title": "Hello World!"\n}\n```\n\nThe exporter will add the following front matter to the generated Markdown:\n\n```text\n---\nlayout: notebook\npermalink: /hello/\ntitle: Hello World!\n---\n```\n\n## Options\n\nSince `jekyllnb` extends `nbconvert`, all existing options are supported. The following new options are available:\n\n- `--site-dir`: Root directory of your Jekyll site. Markdown (`page-dir`) and image (`image-dir`) folders will be created here if they do not exist.\n- `--page-dir`: Directory for generated Markdown files (e.g. _pages or _posts).\n- `--image-dir`: Directory for images. Images are organized into folders for each notebook by default.\nAlias for the `nbconvert` option `NbConvertApp.output_files_dir`.\n- `--no-auto-folder`: Flag to turn off the default behavior of organizing images by notebook name within `image-dir`. (default: `false`)\n\n## nbconvert\n\nJekyllNB also supports `nbconvert` by registering an entry point for the exporter.\nYou can use the Jekyll exporter with `nbconvert` by calling `jupyter nbconvert --to jekyll`.\n\n**Note**: The options above are not available with `nbconvert`.\n',
    'author': 'Kevin Lane',
    'author_email': 'lane.kevin.a@gmail.com',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/klane/jekyllnb',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
