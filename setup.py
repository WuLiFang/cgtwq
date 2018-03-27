"""Python setup script.  """
from setuptools import setup, find_packages
from cgtwq import __about__

setup(
    name='cgtwq',
    version=__about__.__version__,
    author=__about__.__author__,
    packages=find_packages(),
    install_requires=[
        'requests==2.18.4',
        'websocket-client==0.47.0',
    ]
)
