from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()

setup(
    name='lomosplit',
    version='1.0.0',
    description='Utility for splitting LomoKino film scans',
    license='MIT',
    long_description=long_description,
    long_description_content_type='text/markdown',
    author='Egor Malykh',
    author_email='fnk@fea.st',
    url='https://github.com/meownoid/lomosplit',
    packages=['lomosplit'],
    install_requires=[
        'natsort',
        'numpy',
        'scikit-image'
    ]
)
