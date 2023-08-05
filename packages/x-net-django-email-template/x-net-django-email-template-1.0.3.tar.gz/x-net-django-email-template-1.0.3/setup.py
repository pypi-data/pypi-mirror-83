from setuptools import (
    find_packages,
    setup,
)

import x_net_django_email_template

with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    version=x_net_django_email_template.__version__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=find_packages(),
    python_requires=">=3.6",
    classifiers=[
        "Framework :: Django :: 2.2",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
