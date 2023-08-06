import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='dask-k8',
    version='0.1.1',
    license='GPL',
    author="Benoit Seguin",
    url='https://github.com/impresso/dask_k8',
    description='Simple library to start a Dask cluster on Kubernetes',
    packages=find_packages(),
    python_requires='>=3.6',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    install_requires=[
      'requests>=2.20',
      'kubernetes>=9.0,<10',
      'dask[complete]'
    ],
    long_description=README,
    long_description_content_type='text/markdown'
)
