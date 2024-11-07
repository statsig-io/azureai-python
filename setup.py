import os
from setuptools import setup

with open(
    os.path.join(os.path.abspath(os.path.dirname(__file__)), 'README.md'),
    encoding='utf-8'
) as r:
    README = r.read()

setup(
    name='azureai-statsig',
    version="0.1.0",
    description='Statsig wrapped Azure AI inference library',
    long_description=README,
    long_description_content_type="text/markdown",
    author='Kenny Yi',
    author_email='kenny@statsig.com',
    url='https://github.com/statsig-io/azureai-python',
    license='ISC',
    classifiers=[
        'Intended Audience :: Developers',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3',
        'Topic :: Software Development :: Libraries'
    ],
    install_requires=[
        'statsig',
        'azure-ai-inference',
    ],
    include_package_data=True,
    packages=['azureai'],
    python_requires='>=3.8',
)
