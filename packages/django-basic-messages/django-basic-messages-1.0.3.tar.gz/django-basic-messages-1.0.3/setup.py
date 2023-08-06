import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

# allow setup.py to be run from any path
os.chdir(os.path.normpath(os.path.join(os.path.abspath(__file__), os.pardir)))

setuptools.setup(
    name="django-basic-messages", # Replace with your own username
    version="1.0.3",
    author="Jonathan Morgan",
    author_email="jonathan.morgan.007@gmail.com",
    description="A simple re-usable Django application for sending and receiving messages from within django.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/jonathanmorgan/django_messages",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 or later (LGPLv3+)",
        "Operating System :: OS Independent",
        "Development Status :: 5 - Production/Stable",
        "Framework :: Django",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Topic :: Utilities"
    ],
    install_requires=[
        "django",
        "django-taggit",
        "python-utilities-jsm",
        "django-basic-config"
    ],
    python_requires='>=3.6',
)
