"""Python setup script.  """
import os
from setuptools import setup, find_packages

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
        'requests>=2.18.4',
        'websocket-client>=0.47.0',
        'wlf>=0.3.9',
        'Qt.py>=1.1.0'
    ],
    dependency_links=[
        ('https://github.com/WuLiFang/wlf/archive/0.3.9.tar.gz'
         '#egg=wlf-0.3.9'),
    ],
)
