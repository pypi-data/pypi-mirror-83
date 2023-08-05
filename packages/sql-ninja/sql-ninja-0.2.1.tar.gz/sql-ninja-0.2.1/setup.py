from setuptools import setup
from glob import glob

from sqlninja import __version__

def requirements_txt():
    return open('requirements.txt').read().split("\n")

setup(
    name='sql-ninja',
    version=__version__,
    author='Scott Pierce',
    author_email='ddrscott@gmail.com',
    description='SQL + Jinja Templates Done Right™',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/ddrscott/sql-ninja',
    packages=['sqlninja'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    install_requires=requirements_txt(),
    entry_points={
        'console_scripts':[
            "sql = sqlninja.main:cli",
        ],
    }
)
