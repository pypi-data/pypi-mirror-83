import io
import setuptools

from py_deploy import __version__


with io.open('README.md') as readme:
    long_description = readme.read()

setuptools.setup(
    name='py_deploy',
    version=__version__,
    author='Mykyta Velykanov',
    author_email='nikitavelykanov@gmail.com',
    description='A simple deployer cmd tool',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/velykanov/py_deploy',
    packages=setuptools.find_packages(),
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.6',
    entry_points="""
        [console_scripts]
        py-deploy=py_deploy.cli_commands:cli
    """,
)
