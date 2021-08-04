from setuptools import setup, find_packages

setup(
    name='newscenter',
    version='3.0.2',
    description='A News Release Application for Django',
    long_description=open('README.rst').read(),

    author='Imaginary Landscape',
    author_email='dbertrand@imagescape.com',
    classifiers=[
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Framework :: Django',
        'Framework :: Django :: 1.11',
        'Framework :: Django :: 2.2',
        'Framework :: Django :: 3.2',
    ],
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
