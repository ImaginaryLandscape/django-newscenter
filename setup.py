from setuptools import setup, find_packages

setup(
    name='newscenter',
    version='1.5.5',
    description='A News Release Application for Django',
    long_description=open('README.rst').read(),

    author='Imaginary Landscape',
    author_email='dbertrand@imagescape.com',

    install_requires=(
        'pillow',
        'easy-thumbnails',
        'feedparser',
        'site_config',
    ),

    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
)
