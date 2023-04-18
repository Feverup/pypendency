from setuptools import setup, find_packages

with open('README.md', 'r') as readme:
    README = readme.read()


setup(
    name='pypendency',
    version='0.3.0',
    packages=find_packages('src'),
    package_dir={'': 'src'},
    author='Fever - Platform Squad',
    author_email='platform@feverup.com',
    description='A dependency injection tool for python',
    long_description=README,
    long_description_content_type='text/markdown',
    license='MIT License',
    url='https://github.com/Feverup/pypendency',
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Operating System :: OS Independent',
        'Topic :: Software Development :: Libraries',
        'Typing :: Typed',
    ],
    python_requires='>=3.7',
    install_requires=[
        'pyyaml',
    ],
    include_package_data=True,
)
