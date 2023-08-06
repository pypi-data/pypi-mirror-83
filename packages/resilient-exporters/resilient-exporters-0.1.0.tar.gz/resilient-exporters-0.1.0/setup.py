"""Resilient-exporters
"""
import setuptools
from distutils.core import setup

install_requires = ["requests"]
all_requires = install_requires + ["pymongo", "elasticsearch"]
docs_requires = all_requires + ["sphinx", "sphinxbootstrap4theme"]

with open("README.md", "r") as readme:
    setup(
        name='resilient-exporters',
        version='0.1.0',
        packages=['resilient_exporters'],
        python_requires='>=3.5',
        setup_requires=["setuptools", "wheel"],
        install_requires=["requests"],
        extras_require={"mongo": ["pymongo"],
                        "elastic": ["elasticsearch[async]"],
                        "all": all_requires,
                        "docs": docs_requires},
        author="Fayçal Arbai",
        author_email="arbai.faycal@gmail.com",
        description="A package to export data to databases resiliently.",
        long_description=readme.read(),
        long_description_content_type="text/markdown",
        url="https://github.com/arbfay/resilient-exporters.git",
        keywords="data-engineering exporter data mongodb elasticsearch",
        license="MIT License",
        project_urls={
            "Documentation": "https://resilient-exporters.readthedocs.io",
            "Source": "https://github.com/arbfay/resilient-exporters.git"
        },
        classifiers=[
        	'Intended Audience :: Developers',
            'Intended Audience :: Education',
            'Intended Audience :: Science/Research',
            "Intended Audience :: Other Audience",
            "License :: OSI Approved :: MIT License",
            "Development Status :: 2 - Pre-Alpha",
            "Programming Language :: Python :: 3.5",
            "Programming Language :: Python :: 3.6",
            "Programming Language :: Python :: 3.7",
            "Programming Language :: Python :: 3.8",
            "Programming Language :: Python :: 3.9",
            "Operating System :: POSIX :: Linux",
            "Operating System :: MacOS",
            "Operating System :: Microsoft :: Windows",
            "Topic :: Database",
            "Topic :: Home Automation",
            "Topic :: Software Development :: Libraries :: Python Modules",
            "Typing :: Typed"
        ]
    )
