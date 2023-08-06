import setuptools
from os import path as os_path

this_directory = os_path.abspath(os_path.dirname(__file__))


def read_file(filename):
    with open(os_path.join(this_directory, filename), encoding='utf-8') as f:
        long_description = f.read()
    return long_description


with open("README.md", "r") as fh:
    long_description = fh.read()


def read_requirements(filename):
    return [line.strip() for line in read_file(filename).splitlines()
          if not line.startswith('#')]


setuptools.setup(
    name="django_istio_opentracing",
    version="0.1.1",
    author="Du Wei",
    author_email="pandorid@gmail.com",
    description="Django opentracing middleware works with k8s and istio",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/wesdu/django-istio-opentracing",
    keywords=['django', 'istio', 'k8s', 'opentracing'],
    packages=setuptools.find_packages(),
    install_requires=read_requirements('requirements.txt'),
    classifiers=[
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
)