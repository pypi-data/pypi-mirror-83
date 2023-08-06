# -*- coding: utf-8 -*-
from setuptools import setup

package_dir = \
{'': 'src'}

packages = \
['facelift']

package_data = \
{'': ['*'], 'facelift': ['data/landmarks/*']}

install_requires = \
['attrs>=20.2.0,<21.0.0',
 'cached-property>=1.5.2,<2.0.0',
 'dlib>=19.21.0,<20.0.0',
 'numpy>=1.19.2,<2.0.0',
 'opencv-python>=4.4.0,<5.0.0',
 'typing-extensions>=3.7.4,<4.0.0']

extras_require = \
{':sys_platform != "win32"': ['python-magic>=0.4.18,<0.5.0'],
 ':sys_platform == "win32"': ['python-magic-bin>=0.4.14,<0.5.0']}

setup_kwargs = {
    'name': 'facelift',
    'version': '0.1.0',
    'description': 'A simple wrapper for face detection and recognition',
    'long_description': '<div style="background-color: #151320; padding: 1rem; margin-bottom: 1rem;">\n  <img alt="Facelift" src="docs/source/_static/assets/images/facelift.png"/>\n</div>\n\n**A wrapper for decent face feature detection and basic face recognition.**\n\n[![Supported Versions](https://img.shields.io/pypi/pyversions/facelift.svg)](https://pypi.org/project/facelift/)\n[![Test Status](https://github.com/stephen-bunn/facelift/workflows/Test%20Package/badge.svg)](https://github.com/stephen-bunn/facelift)\n[![Codecov](https://codecov.io/gh/stephen-bunn/facelift/branch/master/graph/badge.svg?token=xhhZQr8l76)](https://codecov.io/gh/stephen-bunn/facelift)\n[![Documentation Status](https://readthedocs.org/projects/facelift/badge/?version=latest)](https://facelift.readthedocs.io/)\n[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/ambv/black)\n\nFor more details please head over to our [documentation](https://facelift.readthedocs.io/).\n\n```python\nfrom facelift import FullFaceDetector, iter_stream_frames\nfrom facelift.render import draw_line\nfrom facelift.window import opencv_window\n\ndetector = FullFaceDetector()\nwith opencv_window() as window:\n    for frame in iter_stream_frames():\n        for face in detector.iter_faces(frame):\n            for feature, points in face.landmarks.items():\n                frame = draw_line(frame, points)\n\n        window.render(frame)\n```\n\n<div style="display: flex; justify-content: center;">\n  <img alt="Basic Face Detection" src="docs/source/_static/assets/recordings/basic_face_detection.gif" />\n</div>\n',
    'author': 'Stephen Bunn',
    'author_email': 'stephen@bunn.io',
    'maintainer': None,
    'maintainer_email': None,
    'url': 'https://github.com/stephen-bunn/facelift',
    'package_dir': package_dir,
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
