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
        'wlf~=0.5',
        'Qt.py~=1.1'
    ],
    dependency_links=[
        'git+https://github.com/WuLiFang/wlf@0.5.0#egg=wlf-0.5.0',
    ],
)
