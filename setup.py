import sys
from typing import List
from setuptools import setup, find_packages

with open('README.md', 'r') as readme:
    README = readme.read()


def _get_install_requires() -> List[str]:
    requirements = ['pyyaml']
    if sys.version_info < (3, 7):
        requirements.append('dataclasses')

    return requirements


setup(
    name='pypendency',
    version='0.0.2',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    author='Marcos Hernandez Juarez',
    author_email='marcos.hernandez@feverup.com',
    description='A dependency injection tool for python',
    long_description=README,
    long_description_content_type='text/markdown',
    license='MIT License',
    url='https://github.com/Feverup/pypendency',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Typing :: Typed',
    ],
    python_requires='>=3.6',
    install_requires=_get_install_requires(),
    include_package_data=True,
)
