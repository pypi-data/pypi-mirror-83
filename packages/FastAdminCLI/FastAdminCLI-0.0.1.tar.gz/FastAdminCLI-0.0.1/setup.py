
from setuptools import find_packages, setup

with open('README.md', 'r') as fh:
    long_description = fh.read()

setup(
    name='FastAdminCLI',
    version='0.0.1',
    description='A colection of tools for working with FastAdmin project',
    keywords=['FastAdmin', 'Admin Dashboard'],
    url='https://github.com/alphabotics/FastAdminCLI.git',
    author='Quan Vu, Pycoders.vn',
    author_email='info@quanvu.net, admin@pycoders.vn',
    long_description=long_description,
    long_description_content_type='text/markdown',
    packages=find_packages(exclude=('Tests',)),
    python_requires='>=3.6',
    install_requires=[
        'Jinja2>=2.11.2',
        'click>=7.1.2'
    ],
    entry_points={
        'console_scripts': [
            'fastadmin=FastAdminCLI.cli:main',
        ]
    },
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
)
