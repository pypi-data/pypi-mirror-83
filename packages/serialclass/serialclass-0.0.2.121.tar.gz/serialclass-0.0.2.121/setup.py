import setuptools
import serialclass

with open('README.md', 'r') as readme:
    full_description = readme.read()

setuptools.setup(
    name='serialclass',
    version=serialclass.__version__,
    author='Greg Van Aken',
    author_email='gavanaken@gmail.com',
    description='A base class to get well-formatted serialized representations of child classes',
    long_description=full_description,
    long_description_content_type='text/markdown',
    url='https://github.com/gavanaken/serialclass',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
)