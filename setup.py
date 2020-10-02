from setuptools import setup, find_packages

setup(
    name='newscenter',
    version='2.0.19',
    description='A News Release Application for Django',
    long_description=open('README.rst').read(),

    author='Imaginary Landscape',
    author_email='dbertrand@imagescape.com',

    install_requires=(
        'pillow>=7.1.0',
        'easy-thumbnails',
        'feedparser',
        'site_config',
        'django-el-pagination',
    ),

    zip_safe=False,
    include_package_data=True,
    packages=find_packages(),
)
