import codecs

from setuptools import setup

with codecs.open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with codecs.open("VERSION", "r", encoding="utf-8") as fh:
    version = fh.read().strip()


setup(
    name='cgtwq',
    version=version,
    packages=["cgtwq"],
    description='CGTeamWork python client for humans.',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='NateScarlet',
    author_email='NateScarlet@Gmail.com',
    classifiers=[
        'Private :: Do Not Upload',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    url='https://github.com/WuLiFang/cgtwq',
    install_requires=[
        'Qt.py>=1.1 ,<2.0',
        'environs>=4.2.0 ,<4.3.0',
        'requests>=2.19 ,<3.0',
        'websocket-client>=0.47.0, <1.0',
        'deprecated>=1.2.12, <2.0.0',
        'pathlib2-unicode>=3.0.0, <4.0.0',
        'cast-unknown>=0.1.4, <0.2.0',
        "six>=1.11.0, <2.0.0",
    ],
    include_package_data=True,
)
