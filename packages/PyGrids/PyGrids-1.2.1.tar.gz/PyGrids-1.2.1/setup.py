from setuptools import setup

with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='PyGrids',
    author='Pixymon',
    version='1.2.1',
    author_email='nlarsen23.student@gmail.com',
    packages=['grids'],
    install_requires=['numpy'],
    description='Dimensional Data Manipulation and Spreadsheet-like pretty grids.',
    long_description=long_description,
    long_description_content_type='text/markdown'
)