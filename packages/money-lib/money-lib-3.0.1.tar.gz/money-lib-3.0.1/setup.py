import re

from setuptools import setup, find_packages

with open('money/__init__.py', 'r', encoding='utf-8') as init:
    version = re.search('__version__ = [\'"]([^\'"]+)[\'"]', init.read()).group(1)

with open('README.md', 'r', encoding='utf-8') as readme:
    long_description = readme.read()

setup(
    name='money-lib',
    version=version,
    author='Rui Pereira',
    author_email='r4g3baby@gmail.com',
    license='MIT',
    description='Python 3 money lib with decimal precision and currency exchange support.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/r4g3baby/money-lib',
    packages=find_packages(exclude=['tests*']),
    install_requires=['Babel>=2.5.0'],
    extras_require={
        'Django': ['Django>=2.2']
    },
    python_requires='>=3',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ]
)
