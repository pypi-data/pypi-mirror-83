from setuptools import setup

from djservices import __version__ as version


with open('README.md', 'r') as f:
    long_description = f.read()


setup(
    name='dj-services',
    version=version,
    author='Artyom Loskan',
    author_email='artyom.groshev2017@gmail.com',
    description="Bring services to Django",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/artemowkin/dj-services',
    keywords='django services',
    install_requires=['Django >= 3.0.0'],
    include_package_data=True,
    packages=['djservices'],
)
