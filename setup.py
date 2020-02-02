"""Python setup script.  """
import os

from setuptools import find_packages, setup

__about__ = {}
with open(os.path.join(os.path.dirname(__file__),
                       'cgtwq', '__about__.py')) as f:
    exec(f.read(), __about__)  # pylint: disable=exec-used

setup(
    name='cgtwq',
    version=__about__['__version__'],
    author=__about__['__author__'],
    packages=find_packages(),
    install_requires=[
        'requests~=2.19',
        'websocket-client~=0.47',
        'wlf @ git+https://github.com/WuLiFang/wlf@0.5.3#egg=wlf-0.5.3',
        'Qt.py~=1.1',
        'environs~=4.2.0',
        'marshmallow<3.5.0; python_version >= "2" and python_version < "3.4"',
    ],
)
