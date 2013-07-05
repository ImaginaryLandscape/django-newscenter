from setuptools import setup, find_packages

setup(
    name='newscenter',
    version='1.1.1',
    description='A News Release Application for Django',
    long_description=open('README.rst').read(),

    author='Imaginary Landscape',
    author_email='dbertrand@imagescape.com',

    install_requires=(
        'PIL',
        'easy-thumbnails',
        'feedparser',
    ),

    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
)
