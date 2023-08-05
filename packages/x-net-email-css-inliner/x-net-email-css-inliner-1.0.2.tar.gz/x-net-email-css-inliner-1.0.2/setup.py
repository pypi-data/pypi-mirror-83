from setuptools import (
    find_packages,
    setup,
)

import x_net_email_css_inliner


with open("README.md", encoding="utf-8") as f:
    long_description = f.read()

setup(
    version=x_net_email_css_inliner.__version__,
    long_description=long_description,
    long_description_content_type="text/markdown",
    include_package_data=True,
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "beautifulsoup4==4.9.3",
        "requests==2.24.0",
        "tinycss2==1.0.2",
    ],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.6",
        "Topic :: Internet :: WWW/HTTP",
    ],
)
