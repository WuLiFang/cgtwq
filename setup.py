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
        'requests~=2.18',
        'websocket-client~=0.47',
        'wlf~=0.4',
        'Qt.py~=1.1'
    ],
    dependency_links=[
        ('https://github.com/WuLiFang/wlf/archive/0.4.0.tar.gz'
         '#egg=wlf-0.4.0'),
    ],
)
