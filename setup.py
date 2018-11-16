from setuptools import setup, find_packages

setup(
    name='newscenter',
    version='2.0.13',
    description='A News Release Application for Django',
    long_description=open('README.rst').read(),

    author='Imaginary Landscape',
    author_email='dbertrand@imagescape.com',

    install_requires=(
        'pillow',
        'easy-thumbnails',
        'feedparser',
        'site_config',
        'django-endless-pagination>=2.0',
    ),

    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
)
