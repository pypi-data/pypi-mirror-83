# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['zoomrlib']

package_data = \
{'': ['*']}

entry_points = \
{'console_scripts': ['zoomrlib = zoomrlib.cli:main']}

setup_kwargs = {
    'name': 'zoomrlib',
    'version': '1.0.0',
    'description': 'Library to read and write a ZoomR16 project file',
    'long_description': '[![pipeline status](https://gitlab.com/remytms/zoomrlib/badges/master/pipeline.svg)](https://gitlab.com/remytms/zoomrlib/pipelines)\n[![coverage report](https://gitlab.com/remytms/zoomrlib/badges/master/coverage.svg)](https://gitlab.com/remytms/zoomrlib/pipelines)\n\nzoomrlib\n========\n\nzoomrlib is a library that let you read and write a Zoom R16 project\nfile and export it into a JSON file. It provide also a little cli to\nshow content of a Zoom R16 project as text.\n\n\nInstallation\n------------\n\nPython >= 3.6 is needed (older python version may work, but it\'s not\ntested).\n\n```shell\npip install zoomrlib\n```\n\n\nUsage\n-----\n\nMost important information form a project file can be read and write:\n\nFor the hole **project**:\n- name\n- header\n- bitlength\n- protected\n- insert_effect_on\n- tracks\n- master\n\nFor a **track**:\n- file\n- status\n- stereo_on\n- invert_on\n- pan\n- fader\n- chorus_on\n- chorus_gain\n- reverb_on\n- reverb_gain\n- eqhigh_on\n- eqhigh_freq\n- eqhigh_gain\n- eqmid_on\n- eqmid_freq\n- eqmid_qfactor\n- eqmid_gain\n- eqlow_on\n- eqlow_freq\n- eqlow_gain\n\nFor the **master track**:\n- file\n- fader\n\nIn a python program, use it like this:\n\n```python\nimport zoomrlib\n\nwith zoomrlib.open("PRJDATA.ZDT", "r") as file:\n    prjdata = zoomrlib.load(file)\n\nprint(prjdata.name)\nfor track in prjdata.tracks:\n    print(track.file)\nprint(prjdata.master.file)\n```\n\nThe package brings a small binary that let you export ZDT file to json:\n\n```sh\nzoomrlib PRJDATA.ZDT > prjdata.json\n```\n\nOr directly from the library:\n```sh\npython -m zoomrlib PRJDATA.ZDT > prjdata.json\n```\n\n\nThanks\n------\n\nThis library can\'t exist without the huge work and help of\nLeonhard\xa0Schneider (http://www.audiolooper.de/zoom/home_english.shtml).\nThanks for his help. If you are looking to a GUI to manage your Zoom R16\ntake a look at his project.\n',
    'author': 'Rémy Taymans',
    'author_email': 'remytms@tsmail.eu',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://gitlab.com/remytms/zoomrlib',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'entry_points': entry_points,
    'python_requires': '>=3.6,<4.0',
}


setup(**setup_kwargs)
