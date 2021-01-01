from setuptools import setup, find_packages

setup(
    name='lazy-pdf',
    version='0.1.0',
    author='aulaLanguageEducation',
    packages=find_packages(),
    url='https://github.com/aulaLanguageEducation/lazy-pdf',
    license='LICENSE',
    description='Used to turn lazy exercises into lazy worksheets!',
    long_description=open('README.md').read(),
    install_requires=open('requirements.txt').read(),
)